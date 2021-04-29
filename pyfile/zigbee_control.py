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
    #read in friendly name data
    update_friendly_names()
    frnd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frnd_file = os.path.join(frnd_dir, 'friendly_names.xml')
    tree = ET.parse(frnd_file)
    root = tree.getroot()
    friendly_names = []
    for zig_node in root:
        friendly_names.append(zig_node[0].text)
    return friendly_names

#use database file to update friendly name xml
#remove any unseen fns
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
    #check for devices not on network anymore
    fns_new = get_friendly_names()
    return fns

#used to set states of devices, arg is on or off
def set_state(id, arg):
    global client
    fns = get_friendly_names()
    command = "{\"state\":\"" + str(arg) + "\"}"
    client.publish('zigbee2mqtt/' + fns[int[id]] + '/set', command)
    return [str(command),id,arg]

#id given
def set_cl(id):
    #update call light variable
    fns = get_friendly_names()
    #move cl to top of list
    fns.insert(0, fns.pop(int[id]))
    # edit xml file to reflect current fns
    return fns

#returns dictionary
def get_states():
    global client
    # use /opt/zigbee2mqtt/data/state.json
    states = {}
    for fn in fns:
        command = "{\"state\":\"""\"}"
        # Publish command to zigbee device
	# look into topic to retrieve state
        state = client.publish('zigbee2mqtt/' + fn + '/get', command)
        state = state['features']['value_on']
        states[fn] = state
    return states

#id given
def get_state(id):
    return get_states()[get_friendly_names[int(id)]]

#given id
def get_fn(id):
    return get_friendly_names()[int(id)]

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
