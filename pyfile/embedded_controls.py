import sys
import os
import zigbee_control
import ir_control

# zigbee_control_args: id & command

# def get_zigbee_devices():
#   return zigbee_devices

def init_devices():
  ir_blaster = ir_control.init()
  zigbee_devices = zigbee_control.get_friendly_names()
  call_light_filename = os.path.abspath(os.path.dirname(__file__),'..','call_light.txt')
  call_light_file = open(call_light_filename, 'r')
  Lines = call_light_file.readlines()
  if Lines[0] in zigbee_devices:
    call_light = Lines[0]
  return ir_blaster, call_light, zigbee_devices

def main():
  num_args = len(sys.argv)
  # call_light input

if __name__ == "__main__":
  main()
