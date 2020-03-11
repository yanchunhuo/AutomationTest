# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from pojo.app_ui.android.demoProject.demoProjectConfig import DemoProjectConfig
import configparser as ConfigParser
import os

class APP_UI_Android_DemoProject_Read_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,config_file_path):
        if self.__inited is None:
            self.config=self._readConfig(config_file_path)
            self.__inited=True

    def _readConfig(self, configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile,encoding='utf-8')
        demoProjectConfig = DemoProjectConfig()
        demoProjectConfig.init = config.get('isInit','init')
        return demoProjectConfig
