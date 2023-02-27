#
# createElement.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.922Z+08:00
# @last-modified 2023-02-27T11:35:59.274Z+08:00
#
from appium.webdriver.common.appiumby import AppiumBy
from page_objects.element_info import Element_Info
from page_objects.relative_type import Relative_Type
from page_objects.wait_type import Wait_Type
from selenium.webdriver.common.by import By
from typing import Union

class Create_Element:
    
    @classmethod
    def create(cls, locator_type:Union[By,AppiumBy], locator_value:str, expected_value:str=None,
               wait_type:Wait_Type=None, wait_expected_value:str=None, wait_seconds:float=30,
               relative_element:Element_Info=None,relative_type:Relative_Type=None):
        """_summary_

        Args:
            locator_type (Union[By,AppiumBy]): selenium.webdriver.common.by.By、appium.webdriver.common.appiumby.AppiumBy
            locator_value (str): _description_
            expected_value (str, optional): _description_. Defaults to None.
            wait_type (Wait_Type, optional): page_bojects.wait_type.Wait_Type. Defaults to None.
            wait_expected_value (str, optional): _description_. Defaults to None.
            wait_seconds (float, optional): _description_. Defaults to 30.
            relative_element (Element_Info, optional): 相对元素定位，当前仅支持selenium. Defaults to None.
            relative_type (Relative_Type, optional): page_bojects.relative_typeRelative_Type. 相对元素定位，当前仅支持selenium. Defaults to None.

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
        element_info.relative_element=relative_element
        element_info.relative_type=relative_type
        return element_info