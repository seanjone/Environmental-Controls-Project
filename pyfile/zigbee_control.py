"""
Author: Sean Jones
Date: 2/8/2021
Purpose: Control zigbee outlets via python mqtt client.
"""

import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
import os
import json

#create an instance of the mqtt client (ZO1 = zigbee outlet control)
client = mqtt.Client('ZOC')
call_fn = '0x000d6f0005349f80'
fns = []

#changes init zigbee control node once (not every time script is called) and return friendly names
def zigbee_init():
    global client, fns
    # set client log and connect callback functions
    client.on_log = on_log
    client.on_connect = on_connect
    # connect client to mqtt broker running locally on pi
    broker = '127.0.0.1'
    client.connect(broker)
    print('Connecting to broker...')
    update_friendly_names()
    fns = get_friendly_names()
    return fns

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
    global fns
    #read in friendly name data
    update_friendly_names()
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    friendly_names = []
    for zig_node in root:
        print(zig_node[0].text)
        friendly_names.append(zig_node[0].text)
    fns = friendly_names
    return fns

#use database file to update friendly name xml
#remove any unseen fns
def update_friendly_names():
    global call_fn, fns
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
    #check for devices not on network anymore
    fns_new = get_friendly_names()
    for fn in fns:
        if fn not in fns_new:
            fns.remove(fn)
    return fns

#used to set states of devices, arg is on or off
def send_cmd(id, arg):
    global client
    command = "{\"state\":\"" + str(arg) + "\"}"
    client.publish('zigbee2mqtt/' + fns[id] + '/set', command)
    return [str(command),id,arg]

#id given
def set_cl(id):
    global call_fn, fns
    #update call light variable
    call_fn = fns[id]
    #move cl to top of list
    fns.insert(0, fns.pop(fns.index(call_fn)))
    return ["set_cl",id]

#returns dictionary
def get_states():
    global fns, client
    states = {}
    for fn in fns:
        command = "{\"state\":\"""\"}"
        # Publish command to zigbee device
        state = client.publish('zigbee2mqtt/' + fn + '/get', command)
        state = state['features']['value_on']
        states[fn] = state
    return states

#id given
def get_state(id):
    global fns
    return get_states()[fns[int(id)]]

def get_fns():
    return get_friendly_names()

#given id
def get_fn(id):
    return get_fns()[int(id)]

# for testing purposes only
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
