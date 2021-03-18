"""
Author: Sean Jones
Date: 2/8/2021
Purpose: Control zigbee outlets via python mqtt client.
"""

#import mqtt client class
import paho.mqtt.client as mqtt
#import xml ElementTree parser
import xml.etree.ElementTree as ET
import os

#define on_log function for mqtt client
def on_log(client, userdata, level, buf):
    print('Log: ' + buf)

#define on_connect function for mqtt client
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print('Connected')
    else:
        print('Connect failed with rc='+rc)

#read in friendly name data
frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frnd_file = os.path.join(frnd_dir, 'friendly_names.xml') 
tree = ET.parse(frnd_file)
root = tree.getroot()
friendly_names = []
for zig_node in root:
    friendly_names.append(zig_node[0].text)
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
client.publish('zigbee2mqtt/' + friendly_names[1] + '/set', '{"state":"OFF"}')   # publish to Peanut
while True:
    input('Press enter to toggle switch')
    print('Command')
    client.publish('zigbee2mqtt/' + friendly_names[1] + '/set', '{"state":"TOGGLE"}')
