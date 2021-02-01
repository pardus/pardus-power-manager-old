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
        self.signal_connect()

    def signal_connect(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.powersave.connect("clicked",self.powersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)

    def start(self):
        self.window.show_all()

    def run(self,cmd):
        os.system(cmd)
        
    def powersave_event(self,widget):
        self.status.set_label("Current Mode: Powersave")
        self.run("bash profiles/powersave.sh")


    def balanced_event(self,widget):
        self.status.set_label("Current Mode: Balanced")
        self.run("bash profiles/balanced.sh")

    def performance_event(self,widget):
        self.status.set_label("Current Mode: Performance")
        self.run("bash profiles/performance.sh")

Gtk.init()
Main().start()
Gtk.main()
