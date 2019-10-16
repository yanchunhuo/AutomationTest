# -*- coding:utf-8 -*-
from appium import webdriver
from base.read_app_ui_config import Read_APP_UI_Config
from base.app_ui.android.demoProject.app_ui_android_demoProject_read_config import APP_UI_Android_DemoProject_Read_Config
from common.appium.appOperator import AppOperator
class APP_UI_Android_demoProject_Client(object):

    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.config = Read_APP_UI_Config().app_ui_config
            self.demoProjectConfig = APP_UI_Android_DemoProject_Read_Config().config
            self.driver = webdriver.Remote(self.config.appium_hub,desired_capabilities=self.demoProjectConfig.get_desired_capabilities())
            self.appOperator = AppOperator(self.driver)

            self.__inited=True
