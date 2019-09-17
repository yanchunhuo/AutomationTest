# -*- coding:utf-8 -*-
from pojo.demoProjectConfig import DemoProjectConfig
import configparser as ConfigParser

class DemoProjectReadConfig(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config=self._readConfig('config/demoProjectInit.conf')
            self.__inited=True

    def _readConfig(self,configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile,encoding='utf-8')
        demoProjectConfig=DemoProjectConfig()
        demoProjectConfig.url=config.get('servers','url')
        demoProjectConfig.adminUser=config.get('users','adminUser')
        demoProjectConfig.adminUserPassword = config.get('users', 'adminUserPassword')
        demoProjectConfig.normalUser=config.get('users','normalUser')
        demoProjectConfig.normalUserPassword=config.get('users','normalUserPassword')
        demoProjectConfig.closeUser=config.get('users','closeUser')
        demoProjectConfig.closeUserPassword=config.get('users','closeUserPassword')
        return demoProjectConfig