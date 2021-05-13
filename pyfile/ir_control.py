import time
import os

def init():
    return

def send_cmd(button,duration):
    os.system("irsend SEND_START test " + button.upper())
    time.sleep(float(duration))
    os.system("irsend SEND_STOP test " + button.upper())
    return "message sent"
