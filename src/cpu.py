import os

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

def get_cpu_count():
    i = 0
    while os.path.exists("/sys/devices/system/cpu/cpu"+str(i)):
        i+=1
    return i
    
def create_cpu_box(core=0):
   builder=Gtk.Builder()
   os.chdir("/usr/lib/pardus/power-manager/")
   builder.add_from_file("main.ui")
   box=builder.get_object("cpu_box")
   builder.get_object("cpu_label").set_text("CPU"+str(core))
   return box
