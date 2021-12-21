#!/usr/bin/python3
import os
from tools.utils import readfile

class backlight_devices:
    def __init__(self):
        self.name = ""
        self.max_brightness = 0

def get_max_brightness(device_name):
    fd = readfile("/sys/class/backlight/{}/max_brightness".format(device_name))
    return int(fd)

def get_devices():
    return os.listdir("/sys/class/backlight/")

def get_brightness(device_name):
    fd = readfile("/sys/class/backlight/{}/brightness".format(device_name))
    return int(fd)

def set_brightness(device_name,value):
    fd = open("/sys/class/backlight/{}/brightness".format(device_name),"w")
    fd.write(str(int(value)))
    fd.flush()
    fd.close()


