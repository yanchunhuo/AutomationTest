# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.web_ui.demoProject.web_ui_demoProject_read_config import WEB_UI_DemoProject_Read_Config
from base.read_web_ui_config import Read_WEB_UI_Config
from common.selenium.browser_operator import Browser_Operator
from common.selenium.driver_tool import Driver_Tool
class WEB_UI_DemoProject_Client:
    def __init__(self):
        self.config=Read_WEB_UI_Config().web_ui_config
        self.demoProjectConfig=WEB_UI_DemoProject_Read_Config().config

        self.driver = Driver_Tool.get_driver(self.config.selenium_hub, self.config.current_browser)
        self.driver.get(self.demoProjectConfig.web_host + '/')
        self.browser_operator = Browser_Operator(self.driver)
