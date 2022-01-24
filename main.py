from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Parametri
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT'))
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('controlcentre.html')


@socketio.on('publish')
def handle_publish(json_data):
    mqtt.publish(json_data['topic'], json_data['message'])


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)