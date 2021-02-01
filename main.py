#!/usr/bin/python3
import os, sys, subprocess, requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk


class Main:

    def __init__(self):
        self.builder=Gtk.Builder()
        self.builder.add_from_file("main.ui")
        self.window = self.builder.get_object("window")
        self.powersave=self.builder.get_object("powersave")
        self.balanced=self.builder.get_object("balanced")
        self.performance=self.builder.get_object("performance")
        self.status=self.builder.get_object("status")
        self.signal_connect()

    def signal_connect(self):
        self.window.connect("destroy",Gtk.main_quit)
        self.powersave.connect("clicked",self.powersave_event)
        self.balanced.connect("clicked",self.balanced_event)
        self.performance.connect("clicked",self.performance_event)

    def start(self):
        self.window.show_all()

    def run(self,cmd):
        os.system(cmd)
        
    def powersave_event(self,widget):
        self.status.set_label("Current Mode: Powersave")
        self.run("""
	 # Enable Laptop-Mode disk writing
	 echo 5 > /proc/sys/vm/laptop_mode
	 echo 1500 > /proc/sys/vm/dirty_writeback_centisecs

	 # Disable turbo boost
	 echo 1 > /sys/devices/system/cpu/intel_pstate/no_turbo
	 echo 0 > /sys/devices/system/cpu/cpufreq/boost

	 # Disable network powersave
	 for foo in $(ls /sys/class/net) ; 
	 do echo auto > /sys/class/net/$foo/device/power/control
	 done

	 #NMI watchdog should be turned on
	 for foo in /proc/sys/kernel/nmi_watchdog;
	 do echo 0 > $foo;
	 done

	 # Set SATA channel to power saving
	 for foo in /sys/class/scsi_host/host*/link_power_management_policy;
	 do echo min_power > $foo;
	 done

	 # Select Powersave CPU Governor
	 for foo in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor;
	 do echo powersave > $foo;
	 done

	 # Activate PCI autosuspend
	 for foo in /sys/bus/pci/devices/*/power/control;
	 do echo auto > $foo;
	 done

	 # Activate I2C autosuspend
	 for foo in /sys/bus/i2c/devices/*/power/control;
	 do echo auto > $foo;
	 done

	 # Activate audio card power saving
	 # (sounds shorter than 1 seconds will not be played)
	 echo 1 > /sys/module/snd_hda_intel/parameters/power_save
	 echo Y > /sys/module/snd_hda_intel/parameters/power_save_controller

	 # set brightness 33%
	 for foo in /sys/class/backlight/*;
	 do
	   max=$(cat $foo/max_brightness)
	   echo $(($max/3)) > $foo/brightness
	 done
        """)


    def balanced_event(self,widget):
        self.status.set_label("Current Mode: Balanced")
        self.run("""
	 # Enable Laptop-Mode disk writing
	 echo 0 > /proc/sys/vm/laptop_mode
	 echo 1500 > /proc/sys/vm/dirty_writeback_centisecs

	 # Disable turbo boost
	 echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo
	 echo 1 > /sys/devices/system/cpu/cpufreq/boost

	 # Disable network powersave
	 for foo in $(ls /sys/class/net) ; 
	 do echo auto > /sys/class/net/$foo/device/power/control
	 done

	 #NMI watchdog should be turned on
	 for foo in /proc/sys/kernel/nmi_watchdog;
	 do echo 0 > $foo;
	 done

	 # Set SATA channel to power saving
	 for foo in /sys/class/scsi_host/host*/link_power_management_policy;
	 do echo med_power_with_dipm > $foo;
	 done

	 # Select Powersave CPU Governor
	 for foo in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
	 echo powersave > $foo ;
	 done

	 # Activate PCI autosuspend
	 for foo in /sys/bus/pci/devices/*/power/control;
	 do echo auto > $foo;
	 done

	 # Activate I2C autosuspend
	 for foo in /sys/bus/i2c/devices/*/power/control;
	 do echo auto > $foo;
	 done

	 # Disabile audio_card power saving
	 echo 0 > /sys/module/snd_hda_intel/parameters/power_save_controller
	 echo N > /sys/module/snd_hda_intel/parameters/power_save

	 # set brightness 33%
	 for foo in /sys/class/backlight/*;
	 do
	   max=$(cat $foo/max_brightness)
	   echo $(($max*2/3)) > $foo/brightness
	 done
        """)

    def performance_event(self,widget):
        self.status.set_label("Current Mode: Performance")
        self.run("""
	 # Disable laptop mode
	 echo 0 > /proc/sys/vm/laptop_mode
	 echo 500 > /proc/sys/vm/dirty_writeback_centisecs

	 # Enable turbo boost
	 echo 0 > /sys/devices/system/cpu/intel_pstate/no_turbo
	 echo 1 > /sys/devices/system/cpu/cpufreq/boost

	 # Disable network powersave
	 for foo in $(ls /sys/class/net) ; 
	 do echo on > /sys/class/net/$foo/device/power/control
	 done

	 #NMI watchdog should be turned on
	 for foo in /proc/sys/kernel/nmi_watchdog;
	 do echo 1 > $foo;
	 done

	 # Set SATA channel: max performance
	 for foo in /sys/class/scsi_host/host*/link_power_management_policy;
	 do echo max_performance > $foo;
	 done

	 # CPU Governor: Performance
	 for foo in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
	  echo performance > $foo;
	 done 


	 # Disable PCI autosuspend
	 for foo in /sys/bus/pci/devices/*/power/control;
	 do echo on > $foo;
	 done

	 # Disable I2C autosuspend
	 for foo in /sys/bus/i2c/devices/*/power/control;
	 do echo on > $foo;
	 done

	 # Disabile audio_card power saving
	 echo 0 > /sys/module/snd_hda_intel/parameters/power_save_controller
	 echo N > /sys/module/snd_hda_intel/parameters/power_save

	 # set brightness 100%
	 for foo in /sys/class/backlight/*;
	 do
	   max=$(cat $foo/max_brightness)
	   echo $max > $foo/brightness
	 done
        """)

Gtk.init()
Main().start()
Gtk.main()
