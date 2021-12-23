import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
import sys
import locale
import gettext
from tools.utils import asynchronous
from tools.utils import checkIfProcessRunning
from MainWindow import MainWindow

import config
config = config.config()

import tools.profile
import tools.backlight

import datetime

# Translation Constants:
APPNAME = "pardus-power-manager"
TRANSLATIONS_PATH = "/usr/share/locale"
gettext.install(APPNAME, TRANSLATIONS_PATH)

class StatusIcon:
    def __init__(self):

        # Status icon
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.connect("activate", self.status_icon_left_click)
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.update_status_icon()
        self.window = None
        self.brightness_array = [10, 30, 55, 75, 100]

        # Popup menu
        self.menu = Gtk.Menu()

        show = Gtk.MenuItem()
        show.set_label(_("View"))
        show.connect("activate",self.status_icon_left_click)
        self.menu.append(show)

        menu_profile = Gtk.MenuItem()
        self.menu.append(menu_profile)
        self.submenu_profile = Gtk.Menu()
        menu_profile.set_label(_("Power"))
        menu_profile.set_submenu(self.submenu_profile)

        self.menu_profiles = []
        for i in range(5):
            self.profile_item = Gtk.MenuItem()
            self.menu_profiles.append(self.profile_item)
            self.submenu_profile.append(self.profile_item)

        self.menu_profiles[0].connect("activate",self.menu_item_m1_activated)
        self.menu_profiles[1].connect("activate",self.menu_item_m2_activated)
        self.menu_profiles[2].connect("activate",self.menu_item_m3_activated)
        self.menu_profiles[3].connect("activate",self.menu_item_m4_activated)
        self.menu_profiles[4].connect("activate",self.menu_item_m5_activated)

        quit = Gtk.MenuItem()
        quit.set_label(_("Settings"))
        quit.connect("activate", self.exit)
        self.menu.append(quit)

        self.menu.show_all()
        Gtk.main()

    def menu_item_m1_activated(self,item):
        self.set_profile_and_update(0)


    def menu_item_m2_activated(self,item):
        self.set_profile_and_update(1)


    def menu_item_m3_activated(self,item):
        self.set_profile_and_update(2)


    def menu_item_m4_activated(self,item):
        self.set_profile_and_update(3)


    def menu_item_m5_activated(self,item):
        self.set_profile_and_update(4)

    def update_status_icon(self):
        self.status_icon.set_from_icon_name("pardus-pm")
        if checkIfProcessRunning("gnome-shell"):
            self.status_icon.set_from_icon_name("pardus-pm-gnome")


    def set_profile_and_update(self,profile_id):
        tools.profile.set_profile(profile_id)
        for device in tools.backlight.get_devices():
            percent = tools.backlight.get_max_brightness(device)/100
            brightness_value = self.brightness_array[profile_id]*percent
            tools.backlight.set_brightness(device,brightness_value)

        date = datetime.datetime.now()

        open("/var/log/ppm.log","a").write("EVENT=\"status-icon\" DATE=\"{0}\" PROFILE=\"{1}\"\n".format(
            date,
            profile_id)
        )
        if os.path.exists("/run/ppm") and self.window:
            f = open("/run/ppm","w")
            f.write(str(profile_id))
            f.close()

    def status_icon_left_click(self, status_icon):
        self.update_status_icon()
        if not os.path.exists("/run/ppm"):
            self.window = MainWindow()
            self.window.Window.present()

    def right_click_event(self, icon, button, time):
        power_names = ["Extreme Powersave", "Powersave", "Balanced", "Performance", "Extreme Performance"]
        for i in range(5):
            self.menu_profiles[i].set_label(_(power_names[i]))
        current_profile_id = tools.profile.get_current_profile()
        self.menu_profiles[current_profile_id].set_label("["+_(power_names[current_profile_id])+"]")
        self.menu.popup(None, None, None, self.status_icon, button, time)
        self.update_status_icon()

    def exit(self,widget):
        if not os.path.exists("/run/ppm"):
            self.window = MainWindow()
            self.window.Window.present()
            self.window.ui_settings_button_clicked(None)

