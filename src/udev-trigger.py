#!/usr/bin/python3
import sys
import os
import tools.profile
import tools.backlight
import tools.utils
import config
config = config.config()


if not tools.utils.checkIfProcessRunning("pardus-power-manager"):
    sys.exit(0)
if config.get("udev-enabled","True").lower() != "true":
    exit(0)
if tools.profile.get_ac_online():
    profile = config.get("ppm-mode-ac","3")
    tools.profile.set_profile(int(profile))
else:
    profile = config.get("ppm-mode-battery","1")
    tools.profile.set_profile(int(profile))

brightness_array = [10, 30, 55, 75, 100]
for device in tools.backlight.get_devices():
    percent = tools.backlight.get_max_brightness(device)/100
    brightness_value = brightness_array[int(profile)]*percent
    tools.backlight.set_brightness(device,brightness_value)

if os.path.exists("/run/ppm"):
    f = open("/run/ppm","w")
    f.write(profile)
    f.close()

import datetime
date = datetime.datetime.now()

open("/var/log/ppm.log","a").write("EVENT=\"udev-trigger\"\tPOWER_SUPPLY_ONLINE=\"{0}\"\tDATE=\"{1}\"\tPROFILE=\"{2}\"\n".format(
         tools.profile.get_ac_online(),
         date,
         profile)
    )
sys.exit(0)

