__VARS={}

def read_config():
    config = open("/etc/pardus-power-manager.conf","r")
    for line in config.read().split("\n"):
        if "#" in line:
            line = line.split("#")[0]
        if "=" in line:
            variable = line.split("=")[0]
            value = line.split("=")[1]
            __VARS[variable] = value
    config.close()

def get_value(variable):
    if variable in __VARS:
        value = __VARS[variable]
        if value in ["true","false"]:
            return value == "true"
        if value.isnumeric():
            return int(value)
        return value
    return ""

def set_value(variable,value):
    if variable in __VARS:
        if value == True:
            value = "true"
        if value == False:
            value = "false"
        __VARS[variable] = str(value)

def write_config():
    config = open("/etc/pardus-power-manager.conf","w")
    config.write("[main]\n")
    for variable in __VARS.keys():
        config.write("{}={}\n".format(variable,__VARS[variable]))
    config.close()
