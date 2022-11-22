#
# indexPage.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.931Z+08:00
# @last-modified 2022-11-18T11:44:26.152Z+08:00
#

from page_objects.web_ui.demoProject.elements.indexPageElements import IndexPageElements
from page_objects.web_ui.demoProject.pages.searchPage import SearchPage
from common.selenium.browser_operator import Browser_Operator
class IndexPage:
    def __init__(self,browser_operator:Browser_Operator):
        self.browser_operator=browser_operator
        self.index_page_elements=IndexPageElements()
        self.browser_operator.explicit_wait_page_title(self.index_page_elements.title)
        self.browser_operator.get_screenshot('indexPage')

    def _input_search_kw(self,kw):
        self.browser_operator.send_text(self.index_page_elements.search_input,kw)
        self.browser_operator.get_screenshot('input_search_kw')

    def _click_search_button(self):
        self.browser_operator.click(self.index_page_elements.search_button)
        self.browser_operator.get_screenshot('click_search_button')

    def search_kw(self, kw):
        self._input_search_kw(kw)
        self._click_search_button()
        if kw.strip():
            return SearchPage(self.browser_operator,kw+'_百度搜索')
        return IndexPage(self.browser_operator)