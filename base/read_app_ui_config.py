# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from pojo.app_ui_config import APP_UI_Config
import configparser as ConfigParser

class Read_APP_UI_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.app_ui_config=self._readConfig('config/app_ui_config.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile,encoding='utf-8')
        app_ui_config = APP_UI_Config()
        app_ui_config.max_device_pool=configParser.get('test','max_device_pool')
        return app_ui_config
