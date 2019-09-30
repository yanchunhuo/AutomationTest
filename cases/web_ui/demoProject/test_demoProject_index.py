# -*- coding:utf8 -*-
from base.web_ui.demoProject.web_ui_demoProject_client import WEB_UI_DemoProject_Client
from page_objects.web_ui.demoProject.pages.indexPage import IndexPage
from assertpy import assert_that
class TestIndex:
    def setup_class(self):
        self.demoProjectClient = WEB_UI_DemoProject_Client()
        self.indexPage=IndexPage(self.demoProjectClient.browserOperator)

    def test_search_empty_kw(self):
        self.indexPage.search_kw('')
        assert_that(self.indexPage.getElements().title.wait_expected_value).is_equal_to(self.demoProjectClient.browserOperator.getTitle())

    def test_search_kw(self):
        self.indexPage.search_kw('apitest')
        assert_that('apitest_百度搜索').is_equal_to(self.demoProjectClient.browserOperator.getTitle())

    def teardown_class(self):
        self.demoProjectClient.browserOperator.close()