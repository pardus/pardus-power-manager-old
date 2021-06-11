import os

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

def cpucount():
    i = 0
    while os.path.exists("/sys/devices/system/cpu/cpu"+str(i)):
        i+=1
    return i

def is_cpu_enabled(core):
    try:
        f=open("/sys/devices/system/cpu/cpu"+str(core)+"/online","r")
        return "1" in f.read()
    except:
        return True

def change_cpu_status(core,status):
    if not os.path.exists("/sys/devices/system/cpu/cpu"+str(core)+"/online"):
        return False
    f=open("/sys/devices/system/cpu/cpu"+str(core)+"/online","w")
    if status:
        f.write(1)
    else:
        f.write(0)
    return True

def is_turbo_boost_enabled():
    if os.path.exists("/sys/devices/system/cpu/cpufreq/boost"):
        return "1" in open("/sys/devices/system/cpu/cpufreq/boost","r").read()
    elif os.path.exists("/sys/devices/system/cpu/intel_pstate/no_turbo"):
        return "0" in open("/sys/devices/system/cpu/intel_pstate/no_turbo","r").read()
    else:
        return False

def change_turbo_boost_status(status):
    if status:
        if os.path.exists("/sys/devices/system/cpu/cpufreq/boost"):
            open("/sys/devices/system/cpu/cpufreq/boost","w").write("1")
        elif os.path.exists("/sys/devices/system/cpu/intel_pstate/no_turbo"):
            open("/sys/devices/system/cpu/intel_pstate/no_turbo","w").write("0")
    else:
        if os.path.exists("/sys/devices/system/cpu/cpufreq/boost"):
            open("/sys/devices/system/cpu/cpufreq/boost","w").write("0")
        elif os.path.exists("/sys/devices/system/cpu/intel_pstate/no_turbo"):
            open("/sys/devices/system/cpu/intel_pstate/no_turbo","w").write("1")

def get_cpu_governor(core):
    return open("/sys/devices/system/cpu/cpu"+str(core)+"/cpufreq/scaling_governor","r").read()

def get_cpu_governor(core,governor):
    open("/sys/devices/system/cpu/cpu"+str(core)+"/cpufreq/scaling_governor","w").write(governor)

