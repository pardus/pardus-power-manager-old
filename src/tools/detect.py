import os
from tools.utils import readfile

def is_laptop():
    if os.path.isdir("/proc/pmu"):
        return "Battery" in open("/proc/pmu/info","r").read()
    if os.path.exists("/sys/devices/virtual/dmi/id/chassis_type"):
        type = open("/sys/devices/virtual/dmi/id/chassis_type","r").read().strip()
        return type in ["8", "9", "10", "11"]
    for dev in os.listdir("/sys/class/power_supply"):
        if "BAT" in dev:
            return True
    if os.system("whic dmidecode &>/dev/null") == 0:
        chassis_type = subprocess.getoutput("dmidecode --string chassis-type").strip()
        if chassis_type in ["Notebook", "Portable", "Laptop", "Hand Held"]:
            return True
    if os.path.exists("/proc/acpi/battery"):
        return True
    if os.path.isfile("/proc/apm"):
        type = open("/proc/apm","r").read().split(" ")[5]
        return type in ["0xff", "0x80"]
    return False


def is_live():
    return "boot=live" in readfile("/proc/cmdline")

def is_virtual_machine():
    cpuinfo = readfile("/proc/cpuinfo").split("\n")
    for line in cpuinfo:
        if line.startswith("flags"):
            return "hypervisor" in line
    return False

def is_chroot():
    return readfile("/proc/1/mountinfo") != readfile("/proc/self/mountinfo")

def is_docker():
    return "docker" in readfile("/proc/1/cgroup")

def is_root():
    return os.getuid() == 0
