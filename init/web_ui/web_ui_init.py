#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from init.java.java_maven_init import java_maven_init
from init.web_ui.demoProject.demoProjectInit import DemoProjectInit

def web_ui_init():
    """
    初始化必要的数据
    :return:
    """
    # 初始化java依赖的libs
    java_maven_init()
    # demoProject项目初始化
    DemoProjectInit().init()