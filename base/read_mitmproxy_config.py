# @Author  : yanchunhuo
# @Time    : 2020/7/15 17:30
# github https://github.com/yanchunhuo

from ruamel import yaml

class ReadMitmproxyConfig(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.mitmproxy_config=yaml.safe_load(open('config/mitmproxy.yaml','r',encoding='utf-8'))
            self.__inited=True