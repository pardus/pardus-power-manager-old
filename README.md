# Pardus Power Manager
Power manager for pardus. Uses tlp config and udev rule.

## Features:
* Automatic switch power mode (AC/BAT modes)
* 5 different profile
* Screen backlight change support
* Stop charging %80 (if device supported)

## Installation:
```shell
make 
make install
```

## Run from source
Run as root:
```shell
cd src
python3 main.py
```

## Dependencies:
* libc6
* python3
* tlp
* python3-gi
* python3-dbus
* python3-setproctitle
* python3-psutil

