#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from init.api.demoProject.demoProjectInit import DemoProjectInit

def api_init():
    """
    初始化必要的数据
    :return:
    """

    # 初始化demoProject项目基础数据
    DemoProjectInit().init()