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
import signal

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

def stop_signals(signum, frame):
    sys.exit(0)

if __name__ == "__main__":
    setproctitle.setproctitle("pardus-power-manager")
    import config
    config = config.config()
    if tools.detect.is_virtual_machine():
        print("Virtual machine detected!")
    if tools.detect.is_live():
        tools.profile.set_profile(4) # extreme performance mode
    if tools.detect.is_docker() or tools.detect.is_chroot():
        sys.exit(0) # exit if docker or chroot
    if not tools.detect.is_root():
        sys.exit(0) # exit if non-root user.
    if not tools.detect.is_laptop() and not tools.detect.is_virtual_machine():
        tools.profile.set_service_status(False) # Disable service
        if "--gui" in sys.argv:
            # force enable application for some buggy laptops or testing
            if config.get("force-enable-app","false").lower() != "true":
                error_message=_("Your computer does not need power management.")+ "\n"
                error_message+=_("Do you want to enable it anyway?")
                dialog = Gtk.MessageDialog(
                    transient_for=None,
                    flags=0,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.NONE,
                    text=error_message,
                )
                dialog.add_button(_("No"), Gtk.ResponseType.NO)
                dialog.add_button(_("Yes"), Gtk.ResponseType.YES)
                response = dialog.run()
                dialog.destroy()
                if response in (Gtk.ResponseType.YES, Gtk.ResponseType.APPLY,
                    Gtk.ResponseType.OK, Gtk.ResponseType.ACCEPT):
                    config.set("force-enable-app","true")
                    tools.profile.set_service_status(True)
                else:
                    sys.exit(0) # exit application
        elif config.get("force-enable-app","false").lower() != "true":
            sys.exit(0)

    if config.get("is-app-active","true").lower() != "true":
        if "--autostart" in sys.argv:
            sys.exit(0)
    if not os.path.exists("/etc/xdg/autostart/ppm-autostart.desktop"):
        config.set("is-app-active","true")
        os.symlink("/usr/share/pardus/power-manager/ppm-autostart.desktop","/etc/xdg/autostart/ppm-autostart.desktop")
        if not os.path.exists("/lib/udev/rules.d/99-ppm.rules"):
            os.symlink("/usr/share/pardus/power-manager/udev.rules","/lib/udev/rules.d/99-ppm.rules")
    if config.get("low-battery-enabled", "true"):
        tools.profile.start_battery_control()
    signal.signal(signal.SIGINT, stop_signals)
    signal.signal(signal.SIGTERM, stop_signals)
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

