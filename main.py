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
    return render_template('dashboard.html', **getData())


@socketio.on('getData')
def sendResponse():
    dictionary = getData()
    emit('response', dictionary)


def getData():
        cursor = mysql.get_db().cursor()

        # Query
        cursor.execute(''' SELECT Rover.IDRover, Misura.temperatura,Misura.umidita,Misura.timestamp FROM Misura,Rover,Luogo WHERE (Misura.IDRover = Rover.IDRover) 
        AND (Misura.IDLuogo = Luogo.IDLuogo) AND (Misura.IDRover = 1) ORDER BY Misura.timestamp DESC LIMIT 1 ''')
        rv = cursor.fetchall()
    
        dictionary = {
            "temp": int(rv[0][1]), 
            "umi": int(rv[0][2])
        }
        return dictionary

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True, port=4321)

