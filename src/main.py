#!/usr/bin/python3
import dbus
import dbus.mainloop.glib
import dbus.service
import gettext
import cpu
from gi.repository import GObject as gobject
from gi.repository import GLib, Gio, Gtk, Gdk
import os
import sys
import subprocess
import requests
import threading
import gi
gi.require_version('Gtk', '3.0')
gi.require_version("GdkPixbuf", "2.0")
VERSION = "0.1.0"

gettext.install("power-manager", "/usr/share/locale")


def asynchronous(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper


@asynchronous
def read_node():
    while True:
        os.system("cat /tmp/.power-manager")
        m.start(None)


class Main:

    def __init__(self):
        self.profiles = ["xpowersave", "powersave",
                         "balanced", "performance", "xperformance"]

        self.status_icon = Gtk.StatusIcon()
        self.status_icon.connect("popup-menu", self.right_click_event)
        self.win_opened = False
        if os.path.exists("/etc/tlp.d/99-pardus.conf"):
            self.current_mode = os.readlink(
                "/etc/tlp.d/99-pardus.conf").split("/")[-1].split(".")[0]
        else:
            self.current_mode = "balanced"
        self.status_icon.connect("activate", self.start)
        self.update_status_icon(self.current_mode)


    def update_status_icon(self,name="icon"):
        try:
            if name == "xpowersave":
                self.status_icon.set_from_icon_name("pardus-pm-mode1")
            elif name == "powersave":
                self.status_icon.set_from_icon_name("pardus-pm-mode2")
            elif name == "balanced":
                self.status_icon.set_from_icon_name("pardus-pm-mode3")
            elif name == "performance":
                self.status_icon.set_from_icon_name("pardus-pm-mode4")
            elif name == "xperformance":
                self.status_icon.set_from_icon_name("pardus-pm-mode5")
        except:
            pass
    

    def get_mode_name(self, mode):
        if self.current_mode == "xpowersave":
            return "Extreme Powersave"
        if self.current_mode == "powersave":
            return "Powersave"
        if self.current_mode == "balanced":
            return "Balanced"
        if self.current_mode == "performance":
            return "Performance"
        if self.current_mode == "xperformance":
            return "Extreme Performance"

    def create_win(self):
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain("power-manager")
        if not os.path.exists("../res/main.ui"):
            os.chdir("/usr/lib/pardus/power-manager/")
        else:
            os.chdir("../res")
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path("main.css")
        self.builder.add_from_file("main.ui")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.window = self.builder.get_object("window")
        self.xpowersave = self.builder.get_object("Xpowersave")
        self.powersave = self.builder.get_object("powersave")
        self.balanced = self.builder.get_object("balanced")
        self.performance = self.builder.get_object("performance")
        self.xperformance = self.builder.get_object("Xperformance")
        self.mode = self.builder.get_object("mode")
        self.scale = self.builder.get_object("scale")
        self.modeset = self.builder.get_object("modeset")
        adjustment = self.builder.get_object("adjustment1")
        self.window.connect("destroy", self.stop)

        adjustment.set_lower(1.0)
        adjustment.set_upper(5.0)
        adjustment.set_step_increment(1.0)

        # self.window.set_resizable(False)
        # locale
        self.builder.get_object("label_eps").set_label(_("Extreme Powersave"))
        self.builder.get_object("label_eps").set_line_wrap(True)
        self.builder.get_object("label_ps").set_label(_("Powersave"))
        self.builder.get_object("label_b").set_label(_("Balanced"))
        self.builder.get_object("label_pf").set_label(_("Performance"))
        self.builder.get_object("label_epf").set_label(
            _("Extreme Performance"))
        self.builder.get_object("show_basic").set_label(_("Basic"))
        self.builder.get_object("show_core").set_label(_("Core"))

        self.scale.set_draw_value(True)
        self.scale_event_enable = False
        self.signal_connect()
        self.update_ui()
        self.cpu_init()
        self.builder.get_object("window_title").set_title(
            _("Pardus Power Manager"))

        def basic_clicked(widget):
            self.builder.get_object("notebook").set_current_page(0)
            self.builder.get_object("show_basic").hide()
            self.builder.get_object("show_core").show()
            self.builder.get_object("about_menu").popdown()

        def core_clicked(widget):
            self.builder.get_object("notebook").set_current_page(1)
            self.builder.get_object("about_menu").popdown()
            self.builder.get_object("show_core").hide()
            self.builder.get_object("show_basic").show()

        def show_about_menu(widget):
            self.builder.get_object("about_menu").popup()

        def about_clicked(widget):
            b = Gtk.Builder()
            b.set_translation_domain("power-manager")
            b.add_from_file("main.ui")
            win = b.get_object("dialog_about")
            win.set_version(VERSION)
            win.set_name(_("Pardus Power Manager"))
            win.show_all()
            self.builder.get_object("about_menu").popdown()

        self.builder.get_object("show_basic").connect("clicked", basic_clicked)
        self.builder.get_object("show_core").connect("clicked", core_clicked)
        self.builder.get_object("about").connect("clicked", about_clicked)
        basic_clicked(None)
        self.builder.get_object("about_button").connect(
            "clicked", show_about_menu)

    def signal_connect(self):
        self.powersave.connect("clicked", self.powersave_event)
        self.xpowersave.connect("clicked", self.xpowersave_event)
        self.balanced.connect("clicked", self.balanced_event)
        self.performance.connect("clicked", self.performance_event)
        self.xperformance.connect("clicked", self.xperformance_event)
        self.scale.connect("value-changed", self.scale_event)

    def stop(self, window):
        self.win_opened = False
        self.window.hide()

    def start(self, widget):
        if self.win_opened:
            return
        self.create_win()
        self.win_opened = True
        self.window.show()

    def run(self, cmd):
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

    def quit(self, widget):
        sys.exit(0)

    def update_ui(self):
        self.mode.set_label(_("Current mode: ") +
                            _(self.get_mode_name(self.current_mode)))
        self.scale_event_enable = False
        self.scale.set_value(self.profiles.index(self.current_mode)+1)
        self.scale_event_enable = True
        self.update_status_icon(self.current_mode)

    def update_menu(self):
        self.a.set_label(_("Extreme Powersave"))
        self.b.set_label(_("Powersave"))
        self.d.set_label(_("Performance"))
        self.c.set_label(_("Balanced"))
        self.e.set_label(_("Extreme Performance"))

        if self.current_mode == "xpowersave":
            self.a.set_label("[{}]".format(_("Extreme Powersave")))
        if self.current_mode == "powersave":
            self.b.set_label("[{}]".format(_("Powersave")))
        if self.current_mode == "balanced":
            self.c.set_label("[{}]".format(_("Balanced")))
        if self.current_mode == "performance":
            self.d.set_label("[{}]".format(_("Performance")))
        if self.current_mode == "xperformance":
            self.e.set_label("[{}]".format(_("Extreme Performance")))

    def cpu_init(self):
        if not os.path.exists("/sys/devices/system/cpu/cpufreq/boost") and \
           not os.path.exists("/sys/devices/system/cpu/intel_pstate/no_turbo"):
            self.builder.get_object("turboboost_box").hide()

        def enable_turbo(widget):
            self.run("pkexec /usr/lib/pardus/power-manager/cpucli.py turbo 1")
            turbo_button_action()

        def disable_turbo(widget):
            self.run("pkexec /usr/lib/pardus/power-manager/cpucli.py turbo 0")
            turbo_button_action()

        def turbo_button_action():
            if cpu.is_turbo_boost_enabled():
                self.builder.get_object("tboff").hide()
                self.builder.get_object("tbon").show_all()
            else:
                self.builder.get_object("tbon").hide()
                self.builder.get_object("tboff").show_all()
        turbo_button_action()
        i = 0

        self.builder.get_object("tboff").connect("clicked", enable_turbo)
        self.builder.get_object("tbon").connect("clicked", disable_turbo)
        self.builder.get_object("tboff").set_label(_("off"))
        self.builder.get_object("tbon").set_label(_("on"))
        while i < cpu.cpucount():
            box = self.create_cpu_box(i)
            i += 1
            if i % 4 == 1:
                self.builder.get_object("cpubox1").pack_start(box, False, 0, 0)
            elif i % 4 == 2:
                self.builder.get_object("cpubox2").pack_start(box, False, 0, 0)
            elif i % 4 == 3:
                self.builder.get_object("cpubox3").pack_start(box, False, 0, 0)
            else:
                self.builder.get_object("cpubox4").pack_start(box, False, 0, 0)

        def build_combo():
            liststore = Gtk.ListStore(str)
            i = k = 0
            current = cpu.get_cpu_governor(0)
            for g in cpu.get_available_governors(0):
                if len(g.strip()) > 0:
                    liststore.append([g])
                if g == current:
                    k = i
                i += 1
            self.builder.get_object("governor_box").set_model(liststore)
            self.builder.get_object("governor_box").set_active(k)

        def combo_action(widget):
            model = widget.get_model()
            active = widget.get_active()
            governor = model[active][0]
            if governor != cpu.get_cpu_governor(0):
                self.run(
                    "pkexec /usr/lib/pardus/power-manager/cpucli.py governor "+governor)
                build_combo()

        build_combo()
        self.builder.get_object("governor_box").connect(
            "changed", combo_action)

    def create_cpu_box(self, core=0):
        builder = Gtk.Builder()
        builder.add_from_file("main.ui")
        box = builder.get_object("cpu_box")
        builder.get_object("cpu_label").set_text("CPU"+str(core))
        ebut = builder.get_object("cpu_enabled")
        dbut = builder.get_object("cpu_disabled")

        def disable_core(widget):
            self.run(
                "pkexec /usr/lib/pardus/power-manager/cpucli.py cpu "+str(core)+" 0")
            if not cpu.is_cpu_enabled(core):
                ebut.hide()
                dbut.show_all()

        def enable_core(widget):
            self.run(
                "pkexec /usr/lib/pardus/power-manager/cpucli.py cpu "+str(core)+" 1")
            if cpu.is_cpu_enabled(core):
                ebut.show_all()
                dbut.hide()

        if core == 0:
            builder.get_object("cpu_enabled").set_sensitive(False)
        if cpu.is_cpu_enabled(core):
            ebut.show_all()
            dbut.hide()
        else:
            ebut.hide()
            dbut.show_all()
        ebut.connect("clicked", disable_core)
        dbut.connect("clicked", enable_core)
        return box

    def scale_event(self, widget):
        if not self.scale_event_enable:
            return
        value = int(self.scale.get_value())-1
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

    def xpowersave_event(self, widget):
        self.current_mode = "xpowersave"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 20 xpowersave")
        self.update_ui()

    def powersave_event(self, widget):
        self.current_mode = "powersave"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 40 powersave")
        self.update_ui()

    def balanced_event(self, widget):
        self.current_mode = "balanced"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 60 balanced")
        self.update_ui()

    def performance_event(self, widget):
        self.current_mode = "performance"
        self.run("pkexec /usr/lib/pardus/power-manager/setprofile.py 80 performance")
        self.update_ui()

    def xperformance_event(self, widget):
        self.current_mode = "xperformance"
        self.run(
            "pkexec /usr/lib/pardus/power-manager/setprofile.py 100 xperformance")
        self.update_ui()

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()

        show = Gtk.MenuItem()
        show.set_label(_("View"))
        show.connect("activate", self.start)
        self.menu.append(show)

        menu_profile = Gtk.MenuItem()
        self.menu.append(menu_profile)
        self.submenu_profile = Gtk.Menu()
        menu_profile.set_label(_("Power"))
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
        quit.set_label(_("Quit"))
        quit.connect("activate", self.quit)
        self.menu.append(quit)

        self.update_menu()
        self.menu.show_all()

        self.menu.popup(None, None, None, self.status_icon, button, time)


m = Main()
Gtk.init()


class Service(dbus.service.Object):
    def __init__(self, message):
        self._message = message

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName(
            "org.pardus.powermanager", dbus.SessionBus())
        dbus.service.Object.__init__(
            self, bus_name, "/org/pardus/powermanager")
        self._loop = GLib.MainLoop()
        self._loop.run()

    @dbus.service.method("org.pardus.powermanager.show", in_signature='', out_signature='')
    def show(self):
        m.start(None)


class Client():
    def __init__(self):
        bus = dbus.SessionBus()
        service = bus.get_object(
            'org.pardus.powermanager', "/org/pardus/powermanager")
        self.show = service.get_dbus_method(
            'show', 'org.pardus.powermanager.show')

    def run(self):
        self.show()


try:
    import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind('\0pardus-power-manager_gateway_notify_lock')
    service = Service("Pardus Power Manager").run()
except socket.error as e:
    client = Client().run()
    sys.exit(0)

Gtk.main()
