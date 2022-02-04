from time import sleep, time
import paho.mqtt.client as paho
import time

broker="192.168.5.37"
port=1883
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection
while True:
    ret= client1.publish("rasp1/video_feed","on")
    time.sleep(1)