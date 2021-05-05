"""
Author: Sean Jones
Date: 2/8/2021
Purpose: Control zigbee outlets via python mqtt client.
"""

import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
import os
import json
import time

#create an instance of the mqtt client (ZO1 = zigbee outlet control)
client = mqtt.Client('ZOC')
states = {}
messages = {}

#changes init zigbee control node once (not every time script is called) and return friendly names
def zigbee_init():
    global client
    # set client log and connect callback functions
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_message = on_message
    # connect client to mqtt broker running locally on pi
    broker = '127.0.0.1'
    client.connect(broker)
    #print('Connecting to broker...')
    update_friendly_names()
    fns = get_friendly_names()
    for fn in fns:
        try:
            client.subscribe('zigbee2mqtt/' + str(fn))# + '/get')
        except:
            continue
    client.loop_start()
    return fns

#define on_log function for mqtt client
def on_log(client, userdata, level, buf):
    #print('Log: ' + buf)
    return

#define on_connect function for mqtt client
def on_connect(client, userdata, flags, rc):
    #if(rc == 0):
    #    print('Connected\n')
    #else:
    #    print('Connect failed with rc='+rc)
    return

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

#use database file to update friendly name xml
def update_friendly_names():
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    db_file = open('/opt/zigbee2mqtt/data/database.db')
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
                root.append(new_node)
    tree.write(frnd_file)
    return root

#used to set states of devices, arg is on or off
def set_state(id, arg):
    global client
    fns = get_friendly_names()
    command = "{\"state\":\"" + str(arg) + "\"}"
    client.publish('zigbee2mqtt/' + str(fns[int(id)]) + '/set', command)
    return [str(command),id,arg]

#id given
def set_cl(id):
    #update call light variable
    fns_tmp = get_friendly_names()
    #move cl to top of list
    fns_tmp.insert(0, fns_tmp.pop(int(id)))
    fns = []
    for fn in fns_tmp:
        if fn not in fns:
            fns.append(fn)
    # edit xml file to reflect current fns
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    root.clear()
    #for child in root:
    #    root.remove(child)
    for fn in fns:
        new_node = ET.Element('zigbee-node')
        ET.SubElement(new_node, 'friendly_name')
        new_node[0].text = fn
        root.append(new_node)
    #frnd_file2 = os.path.join(frnd_dir, "friendly_names3.xml")
    tree.write(frnd_file)
    return fns

def on_message(client, userdata, message):
    global messages
    messages[message.topic] = json.loads(message.payload.decode('utf-8'))
    #print('\t{}'.format(messages))
    #print('Received state')
import copy
#returns dictionary
def get_states():
    global client, states, messages
    states = {}
    fns = get_friendly_names()
    fns_tmp = copy.deepcopy(fns)
    for i in range(5):
        for fn in fns_tmp:
            command = "{\"state\":\"\"}"
            client.publish('zigbee2mqtt/' + str(fn) + '/get', command)
        time.sleep(1.5)
        for key in messages:
            fn = key.split('/')[1]
            #print(fn,key)
            if fn in fns_tmp:
                fns_tmp.remove(fn)
            states[fn] = messages[key]['state']
        if len(fns_tmp)==0:
            return states
    return states

#id given
def get_state(id):
    return get_states()[get_friendly_names()[int(id)]]

#given id
def get_fn(id):
    return get_friendly_names()[int(id)]

def custom(a,b,c):
	return a, b, c

zigbee_init()

# for testing purposes only
if __name__ == '__main__':
    zigbee_init()    
    while True:
        comm = input('Dev id: ')
        fns = get_friendly_names()
        print(get_states())
        set_state(comm, 'TOGGLE')
        print(get_states())
	
