#!/usr/bin/python3
import sys
import os
import tools.profile
import tools.utils
import config
config = config.config()
if not tools.utils.checkIfProcessRunning("pardus-power-manager"):
    sys.exit(0)
if config.get("udev-enabled","True").lower() != "true":
    exit(0)
if os.environ["POWER_SUPPLY_ONLINE"] == "1":
    profile = config.get("ppm-mode-ac","3")
    tools.profile.set_profile(int(profile))
else:
    profile = config.get("ppm-mode-battery","1")
    tools.profile.set_profile(int(profile))
    
if os.path.exists("/run/ppm"):
    f = open("/run/ppm","w")
    f.write(os.environ["POWER_SUPPLY_ONLINE"])
    f.close()

import time
open("/var/log/ppm.log","a").write("{} {}\n".format(os.environ["POWER_SUPPLY_ONLINE"],time.time()))
sys.exit(0)

