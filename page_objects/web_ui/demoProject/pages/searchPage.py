#
# searchPage.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.931Z+08:00
# @last-modified 2022-11-18T11:44:45.685Z+08:00
#

from common.selenium.browser_operator import Browser_Operator
from page_objects.web_ui.demoProject.elements.searchPageElements import SearchPageElements
class SearchPage:
    def __init__(self,browser_operator:Browser_Operator,title):
        self.browser_operator=browser_operator
        self.search_page_elements=SearchPageElements()
        self.search_page_elements.title.wait_expected_value=title
        self.browser_operator.explicit_wait_page_title(self.search_page_elements.title)
        self.browser_operator.get_screenshot('searchPage')

    def _input_search_kw(self, kw):
        self.browser_operator.send_text(self.search_page_elements.search_input, kw)
        self.browser_operator.get_screenshot('input_search_kw')

    def _click_search_button(self):
        self.browser_operator.click(self.search_page_elements.search_button)
        self.browser_operator.get_screenshot('click_search_button')

    def search_kw(self, kw):
        self._input_search_kw(kw)
        self._click_search_button()
        if kw.strip():
            return SearchPage(self.browser_operator,kw+'_百度搜索')