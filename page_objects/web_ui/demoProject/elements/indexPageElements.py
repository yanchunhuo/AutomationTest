#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from page_objects.create_element import Create_Element
from page_objects.wait_type import Wait_Type as Wait_By
from selenium.webdriver.common.by import By
class IndexPageElements:
    def __init__(self):
        self.path = '/'
        self.title = Create_Element.create(None,None,None,Wait_By.TITLE_IS,'百度一下，你就知道')
        self.search_input = Create_Element.create(By.ID,'kw',wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.search_button =  Create_Element.create(By.ID,'su',wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)