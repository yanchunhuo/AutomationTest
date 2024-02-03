#
# read_api_config.py
# @author yanchunhuo
# @description 
# @created 2023-09-25T09:31:03.633Z+08:00
# @last-modified 2024-02-03T10:33:15.738Z+08:00
# github https://github.com/yanchunhuo

from ruamel import yaml

class ReadAPIConfig(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config=yaml.safe_load(open('config/api_config.yaml','r',encoding='utf-8'))
            
            self.__inited=True