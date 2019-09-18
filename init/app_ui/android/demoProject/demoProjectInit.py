#-*- coding:utf8 -*-
from base.app_ui.android.demoProject.app_ui_android_demoProject_read_config import APP_UI_Android_DemoProject_Read_Config

class DemoProjectInit:
    def __init__(self):
        self._app_ui_android_demoProject_read_config=APP_UI_Android_DemoProject_Read_Config().config

    def init(self):
        if int(self._app_ui_android_demoProject_read_config.init)==0:
            return
        #每次测试前先清除上次构造的数据
        self._deinit()
        #初始化必要的数据，如在数据库中构建多种类型的账号，
        pass

    def _deinit(self):
        #清除构造的数据
        pass