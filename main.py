from socket import socket
from flask import Flask, render_template
from flaskext.mysql import MySQL
import json
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from flask_socketio import emit

app = Flask(__name__)
load_dotenv()

# Parametri
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] =  os.getenv('MYSQL_DATABASE_HOST')

socketio = SocketIO(app)

# Init DB
mysql = MySQL()
mysql.init_app(app)

# Default route
@app.route('/')
def dashboard():    
    return render_template('dashboard.html', **getData(1))


@socketio.on('getData')
def sendResponse():
    dictionary = getData(1)
    emit('response', dictionary)

@socketio.on('getMoreData')
def sendResponse():
    dictionary = getData(7)
    emit('response', dictionary)

@socketio.on('getOggetti')
def sendResponse():
    dictionary = getOggetti()
    emit('responseT', dictionary)

def getData(limit):
    cursor = mysql.get_db().cursor()

    # Query
    cursor.execute(''' SELECT Rover.IDRover, Misura.temperatura,Misura.umidita,Misura.timestamp FROM Misura,Rover,Luogo WHERE (Misura.IDRover = Rover.IDRover) AND (Misura.IDLuogo = Luogo.IDLuogo) AND (Misura.IDRover = 1) ORDER BY Misura.timestamp DESC LIMIT {}'''.format(limit)) 
    rv = cursor.fetchall()
    
    if limit==1:
        dictionary = {
        "temp": int(rv[0][1]), 
        "umi": int(rv[0][2])
    }
    else:
        dictionary = {}
        temp = []
        timestamp = []
        for i in range(len(rv)):
            temp.append(int(rv[i][1]))
            timestamp.append(rv[i][3])
        dictionary = {
            "temp": temp, 
            "timestamp": timestamp
        }
    return dictionary

def getOggetti():
    cursor = mysql.get_db().cursor()
    cursor.execute(''' SELECT Nome, count(*) FROM Tronco, Varieta WHERE Varieta.IDVarieta = Tronco.IDVarieta GROUP BY Nome''')

    rv = cursor.fetchall()
    
    dictionary = {}
    varieta = []
    numero = []
    for i in range(len(rv)):
        varieta.append(rv[i][0])
        numero.append(int(rv[i][1]))
        dictionary = {
            "varieta": varieta, 
            "numero": numero
        }
    return dictionary


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True, port=4321)

