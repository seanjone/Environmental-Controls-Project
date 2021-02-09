"""
Author: Sean Jones
Date: 2/8/2021
Purpose: Control zigbee outlets via python mqtt client.
Note: Will need client.py file from paho-mqtt install on pi
"""

#import mqtt client class
import paho.mqtt.client as mqtt

#define on_log function for mqtt client
def on_log(client, userdata, level, buf):
    print('Log: ' + buf)

#define on_connect function for mqtt client
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print('Connected')
    else:
        print('Connect failed with rc='+rc)

#create an instance of the mqtt client (ZO1 = zigbee outlet 1)
client = mqtt.Client('ZO1')
#set client log and connect callback functions
client.on_log=on_log
client.on_connect=on_connect
#connect client to mqtt broker running locally on pi
broker = '127.0.0.1'
client.connect(broker)
print('Connecting to broker...\n')
#Continuously toggle on command to test
client.publish('zigbee2mqtt/0x000d6f000a76cdff/set', '{"state":"OFF"}')
while True:
    input('Press enter to toggle switch')
    print('Command')
    client.publish('zigbee2mqtt/0x00124b001e71fbf4/set', '{"state":"TOGGLE"}')




