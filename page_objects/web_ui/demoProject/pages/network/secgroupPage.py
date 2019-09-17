#-*- coding:utf-8 -*-
from page_objects.web_ui.demoProject import SecgroupPageElements
class SecgroupPage:
    def __init__(self,browserOperator):
        self._browserOperator=browserOperator
        self._secgroupPageElement=SecgroupPageElements()
        self._browserOperator.explicit_wait_page_title(self._secgroupPageElement.title)
        self._browserOperator.get_screenshot('secgroupPage')

    def search_secgroup(self,keyword):
        self._browserOperator.sendText(self._secgroupPageElement.search,keyword)
        self._browserOperator.get_screenshot('search_secgroup')
