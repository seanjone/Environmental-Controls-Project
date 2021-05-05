import sys
import os
import zigbee_control
import ir_control

def init_devices():
#   doesn't do anything yet
  ir_blaster = ir_control.init()
#   returns list of friendly names
  zigbee_devices = zigbee_control.zigbee_init()
  # # gets friendly name of call light that was stored
  # call_light_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','call_light.txt')
  # call_light_file = open(call_light_filename, 'r')
  # Lines = call_light_file.readlines()
  # if Lines[0].strip() in zigbee_devices:
  #   # returns friendly name of call light if it can be found
  #   call_light = Lines[0].strip()
  #   # removes call light from zigbee devices so it can't be treated as an outlet
  #   zigbee_devices.remove(call_light)
  # elif len(zigbee_devices) > 0:
  #   call_light = zigbee_devices[0]
  #   zigbee_devices.remove(call_light)
  # else:
  #   call_light = None
  return ir_blaster, zigbee_devices #call_light, zigbee_devices

def command(args):
  device = ''.join(c for c in args[0] if not c.isnumeric()).lower()
  nArgs = len(args)-1
  instructions = ("Try one of the following commands:\n"
                  "init\t\tir <arg>\tcustom_ir <arg1> <arg2> <arg3>\n"
                  "get_states\tget_state <id>\tset_state <id> <state>\n"
                  "get_fns\t\tget_fn <id>\tupdate_fns\n"
                  "set_cl <id>\tcustom_zigbee <arg1> <arg2a> <arg2b> <arg3a> <arg3b>")
  commands = {'init':[init_devices,[] if nArgs==0 else None], #inits ir and zigbee devices
              'ir':[ir_control.send_cmd,[args[1]] if nArgs==1 else None], #sends ir command
              'custom_ir':[ir_control.custom,[args[1],args[2],args[3]] if nArgs==3 else None], #dummy program for custom functionality
              #'cl':[zigbee_control.set_state,['0',args[1]] if nArgs==1 else None], #sends outlet command
              #'o':[zigbee_control.set_state,[args[1].replace("cl","0"),args[2]] if nArgs==2 else None], #sends outlet command
              'set_state':[zigbee_control.set_state,[args[1].replace("cl","0"),args[2].upper()] if nArgs==2 else None],
              'get_states':[zigbee_control.get_states,[] if nArgs==0 else None], #states list
              'get_state':[zigbee_control.get_state,[args[1].replace("cl","0")] if nArgs==1 else None], #states[id]
              'get_fns':[zigbee_control.get_friendly_names,[] if nArgs==0 else None], #friendly_names list
              'get_fn':[zigbee_control.get_fn,[args[1].replace("cl","0")] if nArgs==1 else None], #friendly_names[id]
              'update_fns':[zigbee_control.update_friendly_names,[] if nArgs==0 else None], #adds new devices to friendly_names
              'set_cl':[zigbee_control.set_cl,[args[1]] if nArgs==1 else None], #moves call light to top of list
              'custom_zigbee':[zigbee_control.custom,[args[1],args[2:4],args[4:]] if nArgs==5 else None], #dummy program for custom functionality
              'help':[lambda :instructions,[]]
              }
  try:
    cmd = commands[device]
  except KeyError as err:
    return "{} is not a command.\n{}".format(err,instructions)
  try:
    return cmd[0](*cmd[1]) #function_name(parameter1,parameter2,...)
  except ValueError as err:
    return "{} is not a number.".format(err)
  except IndexError as err:
    return "Device does not exist."
  #except TypeError as err:
  #  return "{} does not have the correct number of parameters.\n{}".format(err,instructions)

def main():
  num_args = len(sys.argv)
  if num_args == 1: #only name of program
    print(init_devices())
  else:
    print(command(sys.argv[1:])) #args minus name of program

if __name__ == "__main__":
  main()
