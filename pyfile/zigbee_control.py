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
import sys

#define on_log function for mqtt client
def on_log(client, userdata, level, buf):
    print('Log: ' + buf)

#define on_connect function for mqtt client
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print('Connected\n')
    else:
        print('Connect failed with rc='+rc)

#look through data base file and add any new friendly names to xml file
def get_friendly_names():
    #read in friendly name data
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    friendly_names = []
    for zig_node in root:
        friendly_names.append(zig_node[0].text)
    return friendly_names

if __name__ == '__main__':
    #create an instance of the mqtt client (ZO1 = zigbee outlet 1)
    client = mqtt.Client('ZO1')
    #set client log and connect callback functions
    client.on_log=on_log
    client.on_connect=on_connect
    #connect client to mqtt broker running locally on pi
    broker = '127.0.0.1'
    client.connect(broker)
    print('Connecting to broker...')
    #get command line args for friendly name and command
    friendly_name = sys.argv[1]
    command = sys.argv[2]
    command = "{\"state\":\"" + str(command) +"\"}"
    #Publish command to zigbee device
    client.publish('zigbee2mqtt/' + friendly_name + '/set', command)
    print('Task completed\n')
