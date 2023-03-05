import os
import dbus

from tools.utils import asynchronous, readfile
import datetime
date = datetime.datetime.now()
try:
    log = open("/var/log/ppm.log","a")
except PermissionError:
    print("Erişim reddedildi. Root olarak deneyin.")
def is_support_charge_limit():
    """Charge level limit support"""
    for bat in os.listdir("/sys/class/power_supply/"):
        for file in ["charge_stop_threshold", "charge_control_end_threshold"]:
            if os.path.exists("/sys/class/power_supply/{}/{}".format(bat,file)):
                return True
    return False

def get_current_profile():
    """Get profile name"""
    if not os.path.exists("/etc/tlp.d/99-pardus.conf"):
        return 2
    link = os.readlink("/etc/tlp.d/99-pardus.conf").split("/")[-1].split(".")[0]
    all_profiles = ["xpowersave", "powersave", "balanced", "performance","xperformance"]
    if str(link) in all_profiles:
        return all_profiles.index(link)
    return 2

def is_systemd_running():
    readfile("/proc/1/comm").strip() == "systemd"

def get_charge_limit():
    """Return change limit status"""
    if not os.path.exists("/etc/tlp.d/99-charge.conf"):
        return False
    link = os.readlink("/etc/tlp.d/99-charge.conf").split("/")[-1].split(".")[0]
    return str(link) == "charge-limit"

def get_service_status():
    """Get tlp service status from systemd-dbus"""
    if not is_systemd_running():
        return False
    bus = dbus.SystemBus()
    systemd = bus.get_object(
        'org.freedesktop.systemd1',
        '/org/freedesktop/systemd1'
    )
    manager = dbus.Interface(
        systemd,
        'org.freedesktop.systemd1.Manager'
    )
    return manager.GetUnitFileState("tlp.service") == "enabled"

def get_ac_online():
    if not os.path.exists("/sys/class/power_supply/"):
        return True
    if len(os.listdir("/sys/class/power_supply/")) == 0:
        return True
    for device in get_acpi_power_devices():
        if os.path.exists("/sys/class/power_supply/{}/status".format(device)):
            status = readfile("/sys/class/power_supply/{}/status".format(device)).lower().strip()
            log.write("EVENT=\"battery-status\"\tBATTERY_DEVICE=\"{0}\"\tDATE=\"{1}\"\tSTATUS=\"{2}\"\n".format(
                 device,
                 date,
                 status)
            )
            log.flush()
            if "discharging" in status:
                return False
            elif "not charging" in status:
                return True
            elif "charging" in status:
                return True
            elif "full" in status:
                return True
            elif "empty" in status:
                return False
            elif "unknown" in status:
                return True
    return True

def get_acpi_power_devices():
    devices = []
    for interface in os.listdir("/sys/bus/acpi/devices/"):
        acpi_device = "/sys/bus/acpi/devices/{}/power_supply".format(interface)
        if os.path.exists(acpi_device):
            for device in os.listdir(acpi_device):
                devices.append(device)
    return devices

@asynchronous
def set_profile(profile_id):
    """Replace profile symlink"""
    all_profiles = ["xpowersave", "powersave", "balanced", "performance","xperformance"]
    profile = all_profiles[profile_id]
    if os.path.exists("/etc/tlp.d/99-pardus.conf"):
        os.unlink("/etc/tlp.d/99-pardus.conf")
    os.symlink("../../usr/share/pardus/power-manager/tlp/{}.conf".format(profile),"/etc/tlp.d/99-pardus.conf")
    os.system("tlp start &>/dev/null &")

@asynchronous
def set_charge_limit(limit_status):
    """Replace charge level symlink"""
    if os.path.exists("/etc/tlp.d/99-charge.conf"):
        os.unlink("/etc/tlp.d/99-charge.conf")
    if limit_status:
        limit = "limit"
    else:
        limit = "full"
    os.symlink("../../usr/share/pardus/power-manager/tlp/charge-{}.conf".format(limit),"/etc/tlp.d/99-charge.conf")
    value = "100"
    if limit == "limit":
        value = "80"
    for bat in os.listdir("/sys/class/power_supply/"):
        for file in ["charge_stop_threshold", "charge_control_end_threshold"]:
            if os.path.exists("/sys/class/power_supply/{}/{}".format(bat,file)):
                o = open("/sys/class/power_supply/{}/{}".format(bat,file),"w")
                o.write(value)
                o.flush()
                o.close()
    os.system("tlp start &>/dev/null &")


def set_service_status(status):
    """Enable-disable tlp service with systemd-dbus"""
    if not is_systemd_running():
        return False
    bus = dbus.SystemBus()
    systemd = bus.get_object(
        'org.freedesktop.systemd1',
        '/org/freedesktop/systemd1'
    )
    manager = dbus.Interface(
        systemd,
        'org.freedesktop.systemd1.Manager'
    )
    if status:
        manager.EnableUnitFiles(["tlp.service"], False, True)
        manager.Reload()
        manager.RestartUnit("tlp.service", "fail")
    else:
        manager.StopUnit("tlp.service","replace")
        manager.DisableUnitFiles(["tlp.service"], False)
        manager.Reload()
    return True
