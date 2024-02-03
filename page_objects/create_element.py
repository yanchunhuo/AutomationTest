#
# createElement.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.922Z+08:00
# @last-modified 2024-02-03T11:24:42.440Z+08:00
#
from appium.webdriver.common.appiumby import AppiumBy
from page_objects.element_info import ElementInfo
from page_objects.relative_type import RelativeType
from page_objects.wait_type import WaitType
from selenium.webdriver.common.by import By
from typing import Union

class CreateElement:
    
    @classmethod
    def create(cls, locator_type:Union[By,AppiumBy], locator_value:str, expected_value:str=None,
               wait_type:WaitType=None, wait_expected_value:str=None, wait_seconds:float=30,
               relative_element:ElementInfo=None,relative_type:RelativeType=None):
        """_summary_

        Args:
            locator_type (Union[By,AppiumBy]): selenium.webdriver.common.by.By、appium.webdriver.common.appiumby.AppiumBy
            locator_value (str): _description_
            expected_value (str, optional): _description_. Defaults to None.
            wait_type (WaitType, optional): page_bojects.wait_type.WaitType. Defaults to None.
            wait_expected_value (str, optional): _description_. Defaults to None.
            wait_seconds (float, optional): _description_. Defaults to 30.
            relative_element (ElementInfo, optional): 相对元素定位，当前仅支持selenium. Defaults to None.
            relative_type (RelativeType, optional): page_bojects.relative_typeRelative_Type. 相对元素定位，当前仅支持selenium. Defaults to None.

        Returns:
            _type_: _description_
        """
        element_info = ElementInfo()
        element_info.locator_type = locator_type
        element_info.locator_value = locator_value
        element_info.expected_value=expected_value
        element_info.wait_type=wait_type
        element_info.wait_seconds=wait_seconds
        element_info.wait_expected_value=wait_expected_value
        element_info.relative_element=relative_element
        element_info.relative_type=relative_type
        return element_info