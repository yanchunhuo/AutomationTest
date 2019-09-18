# -*- coding:utf-8 -*-
from base.web_ui.demoProject.web_ui_demoProject_read_config import WEB_UI_DemoProject_Read_Config
from base.read_web_ui_config import Read_WEB_UI_Config
from common.selenium.browserOperator import BrowserOperator
from common.selenium.driverTool import DriverTool
from page_objects.web_ui.demoProject.pages.loginPage import LoginPage
class WEB_UI_DemoProject_Client:
    def __init__(self,browserOperator_type=0):
        """
        :param browserOperator_type:0-未登录、1-已登录
        """
        self.config=Read_WEB_UI_Config().web_ui_config
        self.demoProjectConfig=WEB_UI_DemoProject_Read_Config().config

        self.driver = DriverTool.get_driver(self.config.selenium_hub, self.config.current_browser)
        self.driver.get(self.demoProjectConfig.web_host + '/cloud/auth/login/')
        self.browserOperator = BrowserOperator(self.driver)
        if browserOperator_type==1:
            loginPage=LoginPage(self.browserOperator)
            loginPage.login_success(self.demoProjectConfig.normal_username, self.demoProjectConfig.normal_password)