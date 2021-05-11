import time
import lirc

def init():
    return

def send_cmd(button,duration):
    lirc.send_start("sharp",button)
    time.sleep(float(duration))
    lirc.send_stop("sharp",button)
    return "message sent"
