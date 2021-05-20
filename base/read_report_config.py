# @Author  : yanchunhuo
# @Time    : 2020/7/23 17:14
 # github https://github.com/yanchunhuo
from pojo.report_config import Report_Config
import configparser as ConfigParser

class Read_Report_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.report_config=self._readConfig('config/report.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile,encoding='utf-8')
        report_config = Report_Config()
        report_config.api_port=configParser.get('api','api_port')
        report_config.app_ui_start_port=configParser.get('app_ui','app_ui_start_port')
        report_config.web_ui_ie_port = configParser.get('web_ui', 'web_ui_ie_port')
        report_config.web_ui_firefox_port = configParser.get('web_ui', 'web_ui_firefox_port')
        report_config.web_ui_chrome_port = configParser.get('web_ui','web_ui_chrome_port')
        return report_config