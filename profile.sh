def=$(cat /usr/lib/pardus/power-manager/default)
[ "$def" == "" ] && def="balanced"
source "/usr/lib/pardus/power-manager/profiles/$def.sh"
