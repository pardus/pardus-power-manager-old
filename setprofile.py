#!/usr/bin/python3
import os,sys

def set_backlight(percent=100):
    for i in os.listdir("/sys/class/backlight/"):
        max_brightness=int(open("/sys/class/backlight/"+i+"/max_brightness","r").read())
        brightness=int(max_brightness*int(percent)/100)
        run("echo {} > /sys/class/backlight/{}/brightness".format(brightness,i))

def set_profile(name):
    if os.path.exists("/etc/tlp.d/99-pardus.conf"):
        run("rm -fv /etc/tlp.d/99-pardus.conf")
    run("ln -fvs ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(name))
    run("tlp start &")

def run(cmd):
    return os.system(cmd)

set_backlight(sys.argv[1])
set_profile(sys.argv[2])
