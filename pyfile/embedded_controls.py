import sys
import os
import zigbee_control
import ir_control

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

def command():
#   "{toggle,on,off} {cl,o1,o2,...,on}"
  return

def main():
  num_args = len(sys.argv)
  if num_args == 0:
    return init_devices()
  # call_light input

if __name__ == "__main__":
  main()
