#
# searchPageElements.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.931Z+08:00
# @last-modified 2024-02-03T11:25:27.315Z+08:00
#

from page_objects.create_element import CreateElement
from page_objects.wait_type import WaitType as Wait_By
from selenium.webdriver.common.by import By

class SearchPageElements:
    def __init__(self):
        self.path = '/'
        self.title = CreateElement.create(None,None,None,Wait_By.TITLE_IS)
        self.search_input = CreateElement.create(By.ID,'kw',wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.search_button =  CreateElement.create(By.ID,'su',wait_type=Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
