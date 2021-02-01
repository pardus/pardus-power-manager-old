# Disable Laptop-Mode disk writing
echo 0 > /proc/sys/vm/laptop_mode
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

# set brightness 66%
for foo in /sys/class/backlight/*;
do
max=$(cat $foo/max_brightness)
echo $(($max*2/3)) > $foo/brightness
done
