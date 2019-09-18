#-*- coding:utf8 -*-
from init.api.demoProject.demoProjectInit import DemoProjectInit

def api_init():
    """
    初始化必要的数据
    :return:
    """

    # 初始化demoProject项目基础数据
    DemoProjectInit().init()