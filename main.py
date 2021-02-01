#!/usr/bin/python3
import os, sys, subprocess, requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Main:

    def __init__(self):
        self.builder=Gtk.Builder()
        self.builder.add_from_file("main.ui")
        self.window = self.builder.get_object("window")
        self.powersave=self.builder.get_object("powersave")
        self.balanced=self.builder.get_object("balanced")
        self.performance=self.builder.get_object("performance")
        self.status=self.builder.get_object("status")
        self.keep=self.builder.get_object("keep")

        self.signal_connect()
        if os.path.exists("/run/pardus-powersave"):
            self.current_mode=open("/run/pardus-powersave","r").read().split("\n")[0]
        elif os.path.exists("/usr/lib/pardus/power-manager/default"):
            self.current_mode=open("/usr/lib/pardus/power-manager/default","r").read().split("\n")[0]
        else:
            self.current_mode="balanced"
        self.update_ui()

    def signal_connect(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.powersave.connect("clicked",self.powersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)
        self.keep.connect("clicked",self.make_default)

    def start(self):
        self.window.show_all()

    def run(self,cmd):
        os.system(cmd)
        
    def make_default(self,widget):
        open("/usr/lib/pardus/power-manager/default","w").write(self.current_mode)
        self.keep.set_sensitive(False)

    def update_ui(self):
        open("/run/pardus-powersave","w").write(self.current_mode)
        if self.current_mode=="powersave":
            self.status.set_label("Current Mode: Powersave")
        if self.current_mode=="balanced":
            self.status.set_label("Current Mode: Balanced")
        if self.current_mode=="performance":
            self.status.set_label("Current Mode: Performance")
        self.keep.set_sensitive(True)

    def powersave_event(self,widget):
        self.run("bash profiles/powersave.sh")
        self.current_mode="powersave"
        self.update_ui()


    def balanced_event(self,widget):
        self.run("bash profiles/balanced.sh")
        self.current_mode="balanced"
        self.update_ui()

    def performance_event(self,widget):
        self.run("bash profiles/performance.sh")
        self.current_mode="performance"
        self.update_ui()

Gtk.init()
Main().start()
Gtk.main()
