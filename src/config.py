import os
from configparser import ConfigParser


class Config(object):
    def __init__(self, filename, section):
        if not(os.path.exists(filename)):
            raise ValueError("{} does not exist".format(filename))

        parser = ConfigParser()
        parser.read(filename)

        config = parser.items(section)
        config = dict(config)

        for key, item in config.items():
            config[key] = eval(item)

        #set params as attributes
        self.__dict__ = config
