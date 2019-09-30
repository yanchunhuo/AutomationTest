# -*- coding:utf-8 -*-
from pojo.web_ui.demoProject.demoProjectConfig import DemoProjectConfig
import configparser as ConfigParser

class WEB_UI_DemoProject_Read_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config=self._readConfig('config/demoProject/web_ui_demoProject.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile)
        demoProjectConfig = DemoProjectConfig()
        demoProjectConfig.web_host = config.get('servers','web_host')
        demoProjectConfig.init=config.get('isInit','init')
        return demoProjectConfig
