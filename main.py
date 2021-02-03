#!/usr/bin/python3
import os, sys, subprocess, requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Main:

    def __init__(self):
        self.builder=Gtk.Builder()
        os.chdir("/usr/lib/pardus/power-manager/")
        self.builder.add_from_file("main.ui")
        self.window = self.builder.get_object("window")
        self.powersave=self.builder.get_object("powersave")
        self.balanced=self.builder.get_object("balanced")
        self.performance=self.builder.get_object("performance")
        self.mode=self.builder.get_object("mode")

        self.signal_connect()
        self.update_ui()

    def signal_connect(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.powersave.connect("clicked",self.powersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)

    def start(self):
        self.window.show_all()

    def run(self,cmd):
        os.system(cmd)
        
    def update_ui(self):
        self.run("tlp start")
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.current_mode=os.readlink("/etc/tlp.d/99-pardus.conf").split("/")[-1].split(".")[0]
        else:
            self.current_mode="unknown"
        self.mode.set_label("Current mode: "+self.current_mode)

    def powersave_event(self,widget):
        self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="powersave"
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()


    def balanced_event(self,widget):
        self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="balanced"
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()

    def performance_event(self,widget):
        self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="performance"
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()

Gtk.init()
Main().start()
Gtk.main()
