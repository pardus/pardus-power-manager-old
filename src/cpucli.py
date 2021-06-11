#!/usr/bin/python3
import sys
import cpu
if sys.argv[1] == "governor":
    cpu.change_cpu_governor(sys.argv[2],sys.argv[3])
elif sys.argv[1] == "turbo":
    cpu.change_turbo_boost_status(sys.argv[1]=="1")
elif sys.argv[1] == "cpu":
    cpu.change_cpu_status(sys.argv[2],sys.argv[3]==1)
