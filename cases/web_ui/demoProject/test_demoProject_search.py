# -*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.web_ui.demoProject.web_ui_demoProject_client import WEB_UI_DemoProject_Client
from page_objects.web_ui.demoProject.pages.indexPage import IndexPage
from common.hamcrest.hamcrest import assert_that
class TestIndex:
    def setup_class(self):
        self.demoProjectClient = WEB_UI_DemoProject_Client()
        self.searchPage=IndexPage(self.demoProjectClient.browser_operator).search_kw('apitest')

    def test_search_kw(self):
        self.searchPage.search_kw('AutomationTest源码')
        assert_that('AutomationTest源码_百度搜索').is_equal_to(self.demoProjectClient.browser_operator.get_title())

    def teardown_class(self):
        self.demoProjectClient.browser_operator.close()