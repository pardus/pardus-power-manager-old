import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk

import os
import sys
import locale
import subprocess
import tools.backlight
import tools.profile
import gettext
from tools.utils import readfile, asynchronous

import datetime

import config
config = config.config()

VERSION = "0.1.1"

# Translation Constants:
APPNAME = "pardus-power-manager"
TRANSLATIONS_PATH = "/usr/share/locale"
gettext.install(APPNAME, TRANSLATIONS_PATH)

class MainWindow:
    def __init__(self):
        # Gtk Builder
        self.builder = Gtk.Builder()

        # Translate things on glade:
        self.builder.set_translation_domain(APPNAME)

        # Import UI file:
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade")

        # Window
        self.Window = self.builder.get_object("ui_main_window")
        self.Window.set_title (_("Pardus Power Manager"))
        self.Window.set_position(Gtk.WindowPosition.CENTER)
        self.Window.connect("destroy", self.onDestroy)
        self.is_running = True


        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        css = "button.radio {border:none}"
        provider.load_from_data(bytes(css,"UTF-8"))


        # Show Screen:
        self.Window.show_all()

        # Hide back button
        self.builder.get_object("ui_button_main").hide()
        if not tools.profile.is_support_charge_limit():
            self.builder.get_object("ui_battery_limit_settings").hide()

        ##################################################################################
        ##################################################################################

        ###
        ###   BACKLIGHT SETTINGS
        ###

        # Get backlight devices
        bl_devices = tools.backlight.get_devices()
        self.backlight_devices = []
        for i in bl_devices:
            bl_device = tools.backlight.backlight_devices()
            bl_device.name = i
            bl_device.max_brightness = tools.backlight.get_max_brightness(i)
            self.backlight_devices.append(bl_device)

        # Get devices backlight value
        if len(self.backlight_devices) > 0:
            backlight_value = tools.backlight.get_brightness(self.backlight_devices[0].name)
            backlight_max_brightness = self.backlight_devices[0].max_brightness
            devices_backlight_percent = round((100*backlight_value)/backlight_max_brightness)
        else:
            devices_backlight_percent = 0
            backlight_max_brightness = 0
            backlight_value = 0

        # Set backlight value to gtk-scale(slider)
        self.ui_gtk_scale = self.builder.get_object("ui_gtk_scale")
        self.ui_gtk_scale.set_value(devices_backlight_percent)

        ##################################################################################
        ##################################################################################

        ###
        ###   POWER MODE SETTINGS
        ###

        # import power mode radio buttons
        self.ui_power_button_array = []
        for i in range(5):
            self.ui_power_button_array.append(self.builder.get_object("ui_radio_button_m{}".format(i+1)))
        self.brightness_array = [10, 30, 55, 75, 100]

        # Get power mode status
        self.power_mode = tools.profile.get_current_profile()

        # Set power buttons
        self.app_wakeup = True
        self.ui_power_button_array[self.power_mode].set_active(True)

        ##################################################################################
        ##################################################################################


        charge_limit = tools.profile.get_charge_limit()
        self.builder.get_object("ui_limit_battery").set_state(charge_limit)
        mode_ac = config.get("ppm-mode-ac","3")
        mode_bat = config.get("ppm-mode-battery","1")
        low_battery_mode = config.get("low-battery-profile","0")
        low_battery_threshold = config.get("low-battery-threshold", "20")
        low_battery_state = config.get("low-battery-enabled", "true").lower() == "true"
        self.builder.get_object("ui_mode_battery").set_active_id(mode_bat)
        self.builder.get_object("ui_mode_ac").set_active_id(mode_ac)
        self.builder.get_object("ui_low_battery_mode").set_active_id(low_battery_mode)
        self.builder.get_object("ui_low_battery").set_state(low_battery_state)
        self.builder.get_object("ui_low_battery_threshold").set_active_id(low_battery_threshold)

        udev_enabled = (config.get("udev-enabled","True").lower() == "true")
        self.builder.get_object("ui_udev_enabled").set_state(udev_enabled)
        self.builder.get_object("ui_udev_settings").set_sensitive(udev_enabled)
        self.builder.get_object("ui_low_battery_mode").set_sensitive(low_battery_state)
        self.builder.get_object("ui_low_battery_threshold").set_sensitive(low_battery_state)

        ##################################################################################
        ##################################################################################

       ### Signal connect after all

        self.builder.connect_signals(self)
        self.update_ui()


    # Window methods:
    def onDestroy(self, action):
        if os.path.exists("/run/ppm"):
            os.unlink("/run/ppm")
        self.is_running = False

    # When Slider Changed
    def on_ui_gtk_scale_value_changed(self,range):
        if not self.app_wakeup:
            return
        for i in self.backlight_devices:
            percent = i.max_brightness/100
            brightness_value = range.get_value()*percent
            tools.backlight.set_brightness(i.name, brightness_value)

    # set slider value
    def set_slider_value(self, value, update_brightness = False):
        self.app_wakeup = False
        if not update_brightness:
            return
        for i in self.backlight_devices:
            percent = i.max_brightness/100
            brightness_value = value*percent
            tools.backlight.set_brightness(i.name, brightness_value)
            self.ui_gtk_scale.set_value(value)
            self.app_wakeup = True


    # When Radio Button Clicked
    def ui_radio_button_m1_toggled(self, toggle_button):
        if(toggle_button.get_active()):
            self.ui_radio_button_event(0)

    def ui_radio_button_m2_toggled(self, toggle_button):
        if(toggle_button.get_active()):
            self.ui_radio_button_event(1)

    def ui_radio_button_m3_toggled(self, toggle_button):
        if(toggle_button.get_active()):
            self.ui_radio_button_event(2)

    def ui_radio_button_m4_toggled(self, toggle_button):
        if(toggle_button.get_active()):
            self.ui_radio_button_event(3)

    def ui_radio_button_m5_toggled(self, toggle_button):
        if(toggle_button.get_active()):
            self.ui_radio_button_event(4)

    def ui_radio_button_event(self,profile_id):
        tools.profile.set_profile(profile_id)
        self.set_slider_value(self.brightness_array[profile_id])
        self.write_log(profile_id)


    ##################################################################################
    # Settings
    ##################################################################################

    def ui_settings_button_clicked(self, button):
        self.builder.get_object("ui_stack_main").set_visible_child_name("settings")
        self.builder.get_object("ui_button_main").show()
        self.builder.get_object("ui_button_settings").hide()


    def ui_back_button_clicked(self, button):
        self.builder.get_object("ui_stack_main").set_visible_child_name("main")
        self.builder.get_object("ui_button_settings").show()
        self.builder.get_object("ui_button_main").hide()

    def ui_service_disable_clicked(self, button):
        tools.profile.set_service_status(False) # Stop & Disable tlp service
        if os.path.exists("/etc/xdg/autostart/ppm-autostart.desktop"):
            os.unlink("/etc/xdg/autostart/ppm-autostart.desktop")
        if os.path.exists("/lib/udev/rules.d/99-ppm.rules"):
            os.unlink("/lib/udev/rules.d/99-ppm.rules")

        config.set("is-app-active","false")
        config.set("force-enable-app","false")
        sys.exit(0) # Exit application

    def ui_limit_battery_state_set(self, switch, state):
        tools.profile.set_charge_limit(state)

    def ui_udev_enabled_state_set(self, switch, state):
        config.set("udev-enabled",str(state))
        self.builder.get_object("ui_udev_settings").set_sensitive(state)

    def ui_low_battery_state_set(self, switch, state):
        config.set("low-battery-enabled", str(state))
        self.builder.get_object("ui_low_battery_mode").set_sensitive(state)
        self.builder.get_object("ui_low_battery_threshold").set_sensitive(state)

    def ui_low_profile_changed(self, combobox):
        config.set("low-battery-profile",combobox.get_active_id())
    
    def ui_low_battery_threshold_changed(self, combobox):
        config.set("low-battery-threshold",combobox.get_active_id())

    def ui_mode_battery_changed(self, combobox):
        config.set("ppm-mode-battery",combobox.get_active_id())

    def ui_mode_ac_changed(self, combobox):
        config.set("ppm-mode-ac",combobox.get_active_id())


    def ui_about_button_clicked(self,button):
        b = Gtk.Builder()
        b.set_translation_domain(APPNAME)
        b.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/../ui/MainWindow.glade")
        win = b.get_object("dialog_about")
        win.set_version(VERSION)
        win.set_program_name(_("Pardus Power Manager"))
        win.show_all()


    def write_log(self,profile):
        date = datetime.datetime.now()

        open("/var/log/ppm.log","a").write("EVENT=\"main-window\"\tPOWER_SUPPLY_ONLINE=\"{0}\"\tDATE=\"{1}\"\tPROFILE=\"{2}\"\n".format(
            tools.profile.get_ac_online(),
            date,
            profile)
        )

    ##################################################################################
    # Ui update fifo trigger
    ##################################################################################

    @asynchronous
    def update_ui(self):
        while True:
            if os.path.exists("/run/ppm"):
                os.unlink("/run/ppm")
            os.mkfifo("/run/ppm",0o600)
            readfile("/run/ppm")
            # Get power mode status
            self.app_wakeup = False
            self.power_mode = tools.profile.get_current_profile()
            
            self.ui_power_button_array[self.power_mode].set_active(True)
            devices_backlight_percent = self.brightness_array[self.power_mode]
            self.set_slider_value(devices_backlight_percent, True)
            self.app_wakeup = True

