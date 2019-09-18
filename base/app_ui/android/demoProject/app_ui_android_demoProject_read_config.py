# -*- coding:utf-8 -*-
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

    def __init__(self):
        if self.__inited is None:
            self.config=self._readConfig('config/demoProject/app_ui_android_demoProject.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile,encoding='utf-8')
        demoProjectConfig = DemoProjectConfig()
        demoProjectConfig.platformName = config.get('desired_capabilities','platformName')
        demoProjectConfig.automationName = config.get('desired_capabilities','automationName')
        demoProjectConfig.platformVersion =  config.get('desired_capabilities','platformVersion')
        demoProjectConfig.deviceName = config.get('desired_capabilities','deviceName')
        demoProjectConfig.appActivity = config.get('desired_capabilities','appActivity')
        demoProjectConfig.appPackage = config.get('desired_capabilities','appPackage')
        demoProjectConfig.app = config.get('desired_capabilities','app')
        demoProjectConfig.init = config.get('isInit','init')
        # 将安装包所在位置转为绝对路径
        if demoProjectConfig.app:
            demoProjectConfig.app = os.path.abspath(demoProjectConfig.app)
        return demoProjectConfig
