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
