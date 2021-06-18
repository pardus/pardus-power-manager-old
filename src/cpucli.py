#!/usr/bin/python3
import sys
import cpu
print(sys.argv[2],sys.argv[3]=="1"
if sys.argv[1] == "governor":
    for i in range(0,cpu.cpucount()):
        cpu.change_cpu_governor(i,sys.argv[2])
elif sys.argv[1] == "turbo":
    cpu.change_turbo_boost_status(sys.argv[1]=="1")
elif sys.argv[1] == "cpu":
    cpu.change_cpu_status(sys.argv[2],sys.argv[3]=="1")
