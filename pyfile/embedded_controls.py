import sys
import os
import test as zigbee_control
import test as ir_control

# zigbee_control_args: id & command

# def get_zigbee_devices():
#   return zigbee_devices

def init_devices():
#   doesn't do anything yet
  ir_blaster = ir_control.init()
#   returns list of friendly names
  zigbee_devices = zigbee_control.init()
#   gets friendly name of call light that was stored
  call_light_filename = os.path.abspath(os.path.dirname(__file__),'..','call_light.txt')
  call_light_file = open(call_light_filename, 'r')
  Lines = call_light_file.readlines()
  if Lines[0] in zigbee_devices:
#     returns friendly name of call light if it can be found
    call_light = Lines[0]
#     removes call light from zigbee devices so it can't be treated as an outlet
    zigbee_devices.remove(call_light)
  elif len(zigbee_devices) > 0:
    call_light = zigbee_devices[0]
    zigbee_devices.remove(call_light)
  else:
    call_light = None
  return ir_blaster, call_light, zigbee_devices

def set_call_light(friendly_name):
  call_light_filename = os.path.abspath(os.path.dirname(__file__),'..','call_light.txt')
  call_light_file = open(call_light_filename, 'w')

def send_cmdA(a, arr):
  return ["cmdA",a,arr]

def send_cmdB(a):
  return ["cmdB",a]

def set_cl(fn):
  return ["set_cl",fn]

def get_states():
  return [4,5]

def get_state(id):
  return 5

def get_fns():
  return [12,15,17,14,13]

def get_fn(id):
  return get_fns()[int(id)]

def command(args):
  device = ''.join(c for c in args[0] if not c.isnumeric())
  commands = {'ir':[ir_control.send_cmdB,args[1:]],
              'cl':[zigbee_control.send_cmdA,['0',args[1:]]],
              'o':[zigbee_control.send_cmdA,[args[1],args[2:]]],
              'set_cl':[zigbee_control.set_cl,[args[1]]],
              'get_states':[zigbee_control.get_states,[]],
              'get_state':[zigbee_control.get_state,[args[1]]],
              'get_fns':[zigbee_control.get_fns,[]],
              'get_fn':[zigbee_control.get_fn,[args[1]]]
              }
  return commands[device][0](*commands[device][1])

def main():
  num_args = len(sys.argv)
  if num_args == 1: #only name of program
    print(init_devices())
  else:
    print(command(sys.argv[1:])) #args minus name of program

if __name__ == "__main__":
  main()
