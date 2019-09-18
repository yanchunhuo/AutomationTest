# -*- coding:utf8 -*-
from base.web_ui.demoProject.web_ui_demoProject_client import WEB_UI_DemoProject_Client
from page_objects.web_ui.demoProject.pages.indexPage import IndexPage
class TestIndex:
    def setup_class(self):
        self.demoProjectClient = WEB_UI_DemoProject_Client(1)
        self.indexPage=IndexPage(self.demoProjectClient.browserOperator)

    def test_click_secgroup_menu(self):
        self.indexPage.click_menu_network()
        self.indexPage.click_menu_network_secgroup()

    def teardown_class(self):
        self.demoProjectClient.browserOperator.close()