# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
class Locator_Type:
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
    IMAGE = "-image"
    ACCESSIBILITY_ID = 'accessibility id'
    IOS_PREDICATE = '-ios predicate string'
    IOS_UIAUTOMATION = '-ios uiautomation'
    IOS_CLASS_CHAIN = '-ios class chain'
    # 仅UiAutomator2可用
    ANDROID_UIAUTOMATOR = '-android uiautomator'
    # 仅Espresso可用
    ANDROID_VIEWTAG = '-android viewtag'
    # 仅Espresso可用
    ANDROID_DATA_MATCHER = '-android datamatcher'