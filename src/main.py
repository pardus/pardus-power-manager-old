#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi, sys, os
from MainWindow import MainWindow
from StatusIcon import StatusIcon

import tools.detect
import tools.profile

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

import setproctitle

import dbus
import dbus.mainloop.glib
import dbus.service

class Service(dbus.service.Object):
    def __init__(self, message):
        self._message = message
        self.statusicon = None

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName(
            "org.pardus.powermanager", dbus.SessionBus())
        dbus.service.Object.__init__(
            self, bus_name, "/org/pardus/powermanager")
        self._loop = GLib.MainLoop()
        tools.profile.set_service_status(True)
        self.statusicon = StatusIcon()
        self._loop.run()

    @dbus.service.method("org.pardus.powermanager.show", in_signature='', out_signature='')
    def show(self):
        if not os.path.exists("/run/ppm"):
            MainWindow()


class Client():
    def __init__(self):
        bus = dbus.SessionBus()
        service = bus.get_object(
            'org.pardus.powermanager', "/org/pardus/powermanager")
        self.show = service.get_dbus_method(
            'show', 'org.pardus.powermanager.show')

    def run(self):
        self.show()

if __name__ == "__main__":
    setproctitle.setproctitle("pardus-power-manager")
    if tools.detect.is_virtual_machine():
        print("Virtual machine detected!")
    elif not tools.detect.is_laptop():
        tools.profile.set_service_status(False) # Disable service
        if "--autostart" not in sys.argv:
            dialog = Gtk.MessageDialog(Gtk.Window(), 
                Gtk.DialogFlags.MODAL,
                Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK,
                ("Your computer dont need power management."))
            dialog.run()
            dialog.destroy()
        sys.exit(0) # exit application
    if tools.detect.is_live():
        tools.profile.set_profile(4) # extreme performance mode
    if tools.detect.is_docker() or tools.detect.is_chroot():
        sys.exit(0) # exit if docker or chroot
    if not tools.detect.is_root():
        sys.exit(0) # exit if non-root user.

    import config
    config = config.config()
    if config.get("is-app-active","true").lower() != "true":
        if "--autostart" in sys.argv:
            sys.exit(0)
    if not os.path.exists("/etc/xdg/autostart/ppm-autostart.desktop"):
        config.set("is-app-active","true")
        os.symlink("/usr/share/pardus/power-manager/ppm-autostart.desktop","/etc/xdg/autostart/ppm-autostart.desktop")
        os.symlink("/usr/share/pardus/power-manager/udev.rules","/lib/udev/rules.d/99-ppm.rules")

    # Dbus server and client for single instange window.
    # /run/ppm fifo file used by gui.
    try:
        import socket
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind('\0pardus-power-manager_gateway_notify_lock')
        if os.path.exists("/run/ppm"):
            os.unlink("/run/ppm")
        service = Service("Pardus Power Manager").run()
    except:
        client = Client().run()
        sys.exit(0)

    Gtk.main()

