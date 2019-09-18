#-*- coding:utf-8 -*-
from page_objects.app_ui.android.demoProject.elements.startPageElements import StartPageElements
from page_objects.app_ui.android.demoProject.pages.indexPage import IndexPage

class StartPage:
    def __init__(self,appOperator):
        self.appOperator=appOperator
        self._startPageElements=StartPageElements()

    def click_start(self):
        self.appOperator.get_screenshot('start_page')
        self.appOperator.click(self._startPageElements.start_btn)

    def searh_city(self,city_name):
        self.appOperator.get_screenshot('search_city_page')
        self.appOperator.sendText(self._startPageElements.search_city,city_name)
        self.appOperator.get_screenshot('search_city_'+city_name)

    def choice_a_city(self):
        city_btns=self.appOperator.getElements(self._startPageElements.city_btns)
        self.appOperator.click(city_btns[2])
        return IndexPage(self.appOperator)

    def getElements(self):
        return self._startPageElements