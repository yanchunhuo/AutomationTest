#
# read_app_ui_monkey_config.py
# @author yanchunhuo
# @description 
# @created 2021-05-18T20:41:36.200Z+08:00
# @last-modified 2021-05-20T18:03:06.125Z+08:00
# github https://github.com/yanchunhuo

from pojo.app_ui_monkey_config import APP_UI_Monkey_Config
import configparser as ConfigParser

class Read_APP_UI_Monkey_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.app_ui_monkey_config=self._readConfig('config/app_ui_monkey.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile,encoding='utf-8')
        app_ui_monkey_config = APP_UI_Monkey_Config()
        app_ui_monkey_config.udid=configParser.get('baseInfo','udid')
        app_ui_monkey_config.phone_ip=configParser.get('baseInfo','phone_ip')
        app_ui_monkey_config.phone_port=configParser.get('baseInfo','phone_port')
        app_ui_monkey_config.package=configParser.get('baseInfo','package')
        app_ui_monkey_config.throttle=configParser.get('baseInfo','throttle')
        app_ui_monkey_config.event_times=configParser.get('baseInfo','event_times')
        return app_ui_monkey_config