#!/usr/bin/python3
import os
if os.getuid() != 0:
    print("You must be root!")
    exit(1)
import sys, subprocess, requests
import gi
gi.require_version('Gtk', '3.0')
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GLib, Gio, Gtk, Gdk


class Main:

    def __init__(self):
        self.profiles=["xpowersave","powersave","balanced","performance","xperformance"]
        self.builder=Gtk.Builder()
        os.chdir("/usr/lib/pardus/power-manager/")
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path("main.css")
        self.builder.add_from_file("main.ui")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.window = self.builder.get_object("window")
        self.xpowersave=self.builder.get_object("Xpowersave")
        self.powersave=self.builder.get_object("powersave")
        self.balanced=self.builder.get_object("balanced")
        self.performance=self.builder.get_object("performance")
        self.xperformance=self.builder.get_object("Xperformance")
        self.mode=self.builder.get_object("mode")
        self.scale = self.builder.get_object("scale")
        adjustment = self.builder.get_object("adjustment1")

        adjustment.set_lower(1.0)
        adjustment.set_upper(5.0)
        adjustment.set_step_increment(1.0)

        self.scale.set_draw_value(True)

        self.scale_event_enable=False
        self.signal_connect()
        self.update_ui()

    def signal_connect(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.powersave.connect("clicked",self.powersave_event)
        self.xpowersave.connect("clicked",self.xpowersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)
        self.xperformance.connect("clicked",self.xperformance_event)
        self.scale.connect("value-changed",self.scale_event)

    def start(self):
        self.window.show_all()

    def run(self,cmd):
        if os.system(cmd) != 0:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Failed to run command",
            )
            dialog.format_secondary_text(
                cmd
            )
            dialog.run()
            dialog.destroy()

    def set_backlight(self,percent=100):
        for i in os.listdir("/sys/class/backlight/"):
            max_brightness=int(open("/sys/class/backlight/"+i+"/max_brightness","r").read())
            brightness=int(max_brightness*percent/100)
            print(brightness)
            os.system("echo {} > /sys/class/backlight/{}/brightness".format(brightness,i))
        
    def update_ui(self):
        self.run("tlp start &")
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.current_mode=os.readlink("/etc/tlp.d/99-pardus.conf").split("/")[-1].split(".")[0]
        else:
            self.current_mode="balanced"
        self.mode.set_label("Current mode: "+self.current_mode)
        self.scale_event_enable = False
        self.scale.set_value(self.profiles.index(self.current_mode)+1)
        self.scale_event_enable = True

    def scale_event(self,widget):
        if not self.scale_event_enable:
            return
        value=int(widget.get_value())-1
        if value == 0:
            self.xpowersave_event(None)
        elif value == 1:
            self.powersave_event(None)
        elif value == 2:
            self.balanced_event(None)
        elif value == 3:
            self.performance_event(None)
        elif value == 4:
            self.xperformance_event(None)


    def xpowersave_event(self,widget):
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="xpowersave"
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.set_backlight(20)
        self.update_ui()

    def powersave_event(self,widget):
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="powersave"
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.set_backlight(40)
        self.update_ui()

    def balanced_event(self,widget):
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="balanced"
        self.set_backlight(60)
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()

    def performance_event(self,widget):
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="performance"
        self.set_backlight(80)
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()

    def xperformance_event(self,widget):
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.run("rm -f /etc/tlp.d/99-pardus.conf")
        self.current_mode="xperformance"
        self.set_backlight(100)
        self.run("ln -s ../../usr/lib/pardus/power-manager/tlp/{}.conf /etc/tlp.d/99-pardus.conf".format(self.current_mode))
        self.update_ui()

Gtk.init()
Main().start()
Gtk.main()
