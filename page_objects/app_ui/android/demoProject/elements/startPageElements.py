#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from page_objects.create_element import CreateElement
from page_objects.wait_type import WaitType as Wait_By
from appium.webdriver.common.appiumby import AppiumBy
class StartPageElements:
    def __init__(self):
        self.start_btn = CreateElement.create(AppiumBy.ID, 'com.moji.mjweather:id/zc', wait_type=Wait_By.VISIBILITY_OF)
        self.search_city = CreateElement.create(AppiumBy.ID, 'com.moji.mjweather:id/d', wait_type=Wait_By.VISIBILITY_OF)
        self.city_btns = CreateElement.create(AppiumBy.ID,'com.moji.mjweather:id/abk',wait_type=Wait_By.VISIBILITY_OF)
