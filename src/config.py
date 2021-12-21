import configparser
import os

class config:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config['PardusPowerManager'] = {}
        if os.path.isfile('/etc/pardus/ppm.conf'):
            self.config.read('/etc/pardus/ppm.conf')

    def get(self,variable,default):
        if variable not in self.config['PardusPowerManager']:
            self.set(variable,default)
            return default
        return self.config['PardusPowerManager'][variable]

    def set(self,varialbe, value):
        self.config['PardusPowerManager'][varialbe] = str(value)
        with open('/etc/pardus/ppm.conf', 'w') as configfile:
            self.config.write(configfile)

config()
