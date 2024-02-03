# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.web_ui.demoProject.web_ui_demoProject_read_config import WEB_UI_DemoProject_Read_Config
from base.read_web_ui_config import ReadWebUiConfig
from common.selenium.browser_operator import Browser_Operator
from common.selenium.driver_tool import DriverTool
class WEB_UI_DemoProject_Client:
    def __init__(self):
        self.config=ReadWebUiConfig().web_ui_config
        self.demoProjectConfig=WEB_UI_DemoProject_Read_Config().config

        self.driver = DriverTool.get_driver(self.config['server']['selenium_hub'], self.config['browser']['current_browser'])
        self.driver.get(self.demoProjectConfig.web_host + '/')
        self.browser_operator = Browser_Operator(self.driver)
