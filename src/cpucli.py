#!/usr/bin/python3
import sys
import cpu
import os
if sys.argv[1] == "governor":
    for i in range(0, cpu.cpucount()):
        cpu.change_cpu_governor(i, sys.argv[2])
elif sys.argv[1] == "turbo":
    cpu.change_turbo_boost_status(sys.argv[2] == "1")
elif sys.argv[1] == "cpu":
    cpu.change_cpu_status(sys.argv[2], sys.argv[3] == "1")
elif sys.argv[1] == "profile":
    os.system("/usr/lib/pardus/power-manager/setprofile.py {} {}".format(sys.argv[2],sys.argv[3]))
elif sys.argv[1] == "clear":
    os.system("echo 3 > /proc/sys/vm/drop_caches")
    os.system("rm -rf /tmp/*")
