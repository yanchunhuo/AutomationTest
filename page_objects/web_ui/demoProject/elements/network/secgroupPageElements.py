#-*- coding:utf-8 -*-
from page_objects.createElement import CreateElement
from page_objects.web_ui.wait_type import Wait_Type as Wait_By
from page_objects.web_ui.locator_type import Locator_Type
class SecgroupPageElements:
    def __init__(self):
        self.title=CreateElement.create(None,None,None,Wait_By.TITLE_IS,'安全组 - 百悟云')
        self.search=CreateElement.create(Locator_Type.NAME,'security_groups__filter__q','筛选',Wait_By.PRESENCE_OF_ELEMENT_LOCATED)