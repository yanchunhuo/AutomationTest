# -*- coding:utf8 -*-
from base.web_ui.demoProject.web_ui_demoProject_client import WEB_UI_DemoProject_Client
from page_objects.web_ui.demoProject.pages.indexPage import IndexPage
from assertpy import assert_that
class TestIndex:
    def setup_class(self):
        self.demoProjectClient = WEB_UI_DemoProject_Client()
        self.searchPage=IndexPage(self.demoProjectClient.browserOperator).search_kw('apitest')

    def test_search_kw(self):
        self.searchPage.search_kw('apitest12')
        assert_that('apitest12_百度搜索').is_equal_to(self.demoProjectClient.browserOperator.getTitle())

    def teardown_class(self):
        self.demoProjectClient.browserOperator.close()