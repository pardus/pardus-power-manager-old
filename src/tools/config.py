__VARS={}

def read_config():
    with open("/etc/pardus-power-manager.conf", "r") as config:
        for line in config.read().split("\n"):
            if "#" in line:
                line = line.split("#")[0]
            if "=" in line:
                variable = line.split("=")[0]
                value = line.split("=")[1]
                __VARS[variable] = value

def get_value(variable):
    value = __VARS.get(variable)
    if value is None:
        return ""
    if value in ["true", "false"]:
        return value == "true"
    if value.isnumeric():
        return int(value)
    return value

def set_value(variable, value):
    if __VARS.get(variable) is None:
        return
    if value == True:
        value = "true"
    if value == False:
        value = "false"
    __VARS[variable] = str(value)

def write_config():
    with open("/etc/pardus-power-manager.conf", "w") as config:
        config.write("[main]\n")
        for variable, value in __VARS.values():
            config.write("{}={}\n".format(variable, value))
