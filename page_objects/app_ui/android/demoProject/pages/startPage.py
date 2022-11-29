#-*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from page_objects.app_ui.android.demoProject.elements.startPageElements import StartPageElements
from page_objects.app_ui.android.demoProject.pages.indexPage import IndexPage

class StartPage:
    def __init__(self,app_operator):
        self.app_operator=app_operator
        self._startPageElements=StartPageElements()

    def click_start(self):
        self.app_operator.get_screenshot('start_page')
        self.app_operator.click(self._startPageElements.start_btn)

    def searh_city(self,city_name):
        self.app_operator.get_screenshot('search_city_page')
        self.app_operator.send_text(self._startPageElements.search_city,city_name)
        self.app_operator.get_screenshot('search_city_'+city_name)

    def choice_a_city(self):
        city_btns=self.app_operator.getElements(self._startPageElements.city_btns)
        self.app_operator.click(city_btns[2])
        return IndexPage(self.app_operator)

    def getElements(self):
        return self._startPageElements