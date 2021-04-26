"""
Author: Sean Jones
Date: 2/8/2021
Purpose: Control zigbee outlets via python mqtt client.
"""
#call light fn: 0x000d6f0005349f80
#import mqtt client class
#import paho.mqtt.client as mqtt
#import xml ElementTree parser
import xml.etree.ElementTree as ET
import os
import sys
import json

#create an instance of the mqtt client (ZO1 = zigbee outlet control)
#client = mqtt.Client('ZOC')
call_fn = '0x000d6f0005349f80'
#changes init zigbee control node once (not every time script is called) and return friendly names
def zigbee_init():
    global client
    # set client log and connect callback functions
    client.on_log = on_log
    client.on_connect = on_connect
    # connect client to mqtt broker running locally on pi
    broker = '127.0.0.1'
    client.connect(broker)
    print('Connecting to broker...')
    update_friendly_names()
    return get_friendly_names()

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
        print(zig_node[0].text)
        friendly_names.append(zig_node[0].text)
    return friendly_names

#use database file to update friendly name xml
def update_friendly_names():
    global call_fn
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    db_file = open('database.db')
    curr_devices = []
    curr_fns = get_friendly_names()
    for obj in db_file:
        curr_devices.append(json.loads(obj))
    for dev in curr_devices:
        _type = dev['type']
        if _type == 'Router':
            fn = dev['ieeeAddr']
            if fn not in curr_fns:
                new_node = ET.Element('zigbee-node')
                ET.SubElement(new_node, 'friendly_name')
                new_node[0].text = fn
                if fn == call_fn:
                    ET.SubElement(new_node, 'usage')
                    new_node[1].text = "Call light device"
                root.append(new_node)
    tree.write(frnd_file)
    return 0

def send_cmd(id, arg):
  return ["cmdA",id,arg]

#move fn to top (call light)
def set_cl(id):
  return ["set_cl",id]

def get_states():
  return [4,5]

def get_state(id):
  return 5

def get_fns():
  return [12,15,17,14,13]

def get_fn(id):
  return get_fns()[int(id)]

if __name__ == '__main__':
    #get command line args for friendly name and command
    #script called with ID not friendly name
    #call light is 0
    #friendly_name = sys.argv[1]
    #command = sys.argv[2]
    #command = "{\"state\":\"" + str(command) +"\"}"
    #Publish command to zigbee device
    #client.publish('zigbee2mqtt/' + friendly_name + '/set', command)
    update_friendly_names()
    print('Task completed\n')
