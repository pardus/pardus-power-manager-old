#!/usr/bin/python3
import os
import sys, subprocess, requests
import gi
gi.require_version('Gtk', '3.0')
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GLib, Gio, Gtk, Gdk

try:
    import socket

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind('\0pardus-power-manager_gateway_notify_lock')
except socket.error as e:
    error_code = e.args[0]
    error_string = e.args[1]
    dialog = Gtk.MessageDialog(
                transient_for=Gtk.Window(),
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Process already running in background.",
            )
    dialog.run()
    dialog.destroy()
    sys.exit(0)


class Main:

    def __init__(self):
        self.profiles=["xpowersave","powersave","balanced","performance","xperformance"]
        self.builder=Gtk.Builder()
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_file("/usr/lib/pardus/power-manager/icon.svg")
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.win_opened=False
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.current_mode=os.readlink("/etc/tlp.d/99-pardus.conf").split("/")[-1].split(".")[0]
        else:
            self.current_mode="balanced"



    def create_win(self):
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
        self.modeset = self.builder.get_object("modeset")
        adjustment = self.builder.get_object("adjustment1")
        self.window.connect("destroy",self.stop)

        adjustment.set_lower(1.0)
        adjustment.set_upper(5.0)
        adjustment.set_step_increment(1.0)

        self.scale.set_draw_value(True)
        self.scale_event_enable=False
        self.signal_connect()
        self.update_ui()

    def signal_connect(self):
        self.powersave.connect("clicked",self.powersave_event)
        self.xpowersave.connect("clicked",self.xpowersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)
        self.xperformance.connect("clicked",self.xperformance_event)
        self.scale.connect("value-changed",self.scale_event)
        self.modeset.connect("clicked",self.modeset_event)


    def stop(self,window):
        self.win_opened=False
        self.window.hide()

    def start(self,widget):
        if self.win_opened:
            return
        self.create_win()
        self.win_opened=True
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


    def modeset_event(self,widget):
        nb=self.builder.get_object("notebook")
        cur_page=nb.get_current_page()
        if cur_page == 0:
            nb.set_current_page(1)
            widget.set_label("Basic")
        else:
            nb.set_current_page(0)
            widget.set_label("Core")

        
    def update_ui(self):
            self.mode.set_label("Current mode: "+self.current_mode)
            self.scale_event_enable = False
            self.scale.set_value(self.profiles.index(self.current_mode)+1)
            self.scale_event_enable = True
      
    def update_menu(self):
        self.a.set_label("Extreme Powersave")
        self.b.set_label("Powersave")
        self.d.set_label("Performance")
        self.c.set_label("Balanced")
        self.e.set_label("Extreme Performance")

        if self.current_mode=="xpowersave":
            self.a.set_label("[Extreme Powersave]")
        if self.current_mode=="powersave":
            self.b.set_label("[Powersave]")
        if self.current_mode=="balanced":
            self.c.set_label("[Balanced]")
        if self.current_mode=="performance":
            self.d.set_label("[Performance]")
        if self.current_mode=="xperformance":
            self.e.set_label("[Extreme Performance]")

    def scale_event(self,widget):
        if not self.scale_event_enable:
            return
        value=int(self.scale.get_value())-1
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
        self.current_mode="xpowersave"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 20 xpowersave")
        self.update_ui()

    def powersave_event(self,widget):
        self.current_mode="powersave"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 40 powersave")
        self.update_ui()

    def balanced_event(self,widget):
        self.current_mode="balanced"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 60 balanced")
        self.update_ui()

    def performance_event(self,widget):
        self.current_mode="performance"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 80 performance")
        self.update_ui()

    def xperformance_event(self,widget):
        self.current_mode="xperformance"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 100 xperformance")
        self.update_ui()

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()

        show = Gtk.MenuItem()
        show.set_label("View")
        show.connect("activate", self.start)
        self.menu.append(show)

        menu_profile=Gtk.MenuItem()
        self.menu.append(menu_profile)
        self.submenu_profile=Gtk.Menu()
        menu_profile.set_label("Power")
        menu_profile.set_submenu(self.submenu_profile)


        self.a = Gtk.MenuItem()
        self.a.connect("activate", self.xpowersave_event)
        self.submenu_profile.append(self.a)

        self.b = Gtk.MenuItem()
        self.b.connect("activate", self.powersave_event)
        self.submenu_profile.append(self.b)

        self.c = Gtk.MenuItem()
        self.c.connect("activate", self.balanced_event)
        self.submenu_profile.append(self.c)

        self.d = Gtk.MenuItem()
        self.d.connect("activate", self.performance_event)
        self.submenu_profile.append(self.d)

        self.e = Gtk.MenuItem()
        self.e.connect("activate", self.xperformance_event)
        self.submenu_profile.append(self.e)

        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", Gtk.main_quit)
        self.menu.append(quit)

        self.update_menu()
        self.menu.show_all()

        self.menu.popup(None, None, None, self.status_icon, button, time)


Gtk.init()
m=Main()
if "show" in sys.argv:
    m.start(None)
Gtk.main()
