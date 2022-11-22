#
# createElement.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.922Z+08:00
# @last-modified 2022-11-21T15:31:41.749Z+08:00
#
from appium.webdriver.common.appiumby import AppiumBy
from page_objects.element_info import Element_Info
from page_objects.wait_type import Wait_Type
from selenium.webdriver.common.by import By
from typing import Union

class Create_Element:
    
    @classmethod
    def create(cls, locator_type:Union[By,AppiumBy], locator_value:str, expected_value:str=None, wait_type:Wait_Type=None, wait_expected_value:str=None, wait_seconds:float=30):
        """_summary_

        Args:
            locator_type (Union[By,AppiumBy]): _description_
            locator_value (str): _description_
            expected_value (str, optional): _description_. Defaults to None.
            wait_type (Wait_Type, optional): _description_. Defaults to None.
            wait_expected_value (str, optional): _description_. Defaults to None.
            wait_seconds (float, optional): _description_. Defaults to 30.

        Returns:
            _type_: _description_
        """
        element_info = Element_Info()
        element_info.locator_type = locator_type
        element_info.locator_value = locator_value
        element_info.expected_value=expected_value
        element_info.wait_type=wait_type
        element_info.wait_seconds=wait_seconds
        element_info.wait_expected_value=wait_expected_value
        return element_info