#-*- coding:utf8 -*-
from init.java.java_maven_init import java_maven_init
from init.app_ui.android.demoProject.demoProjectInit import DemoProjectInit

def android_init():
    """
    初始化android项目必要的数据
    :return:
    """
    # 初始化java依赖的libs
    java_maven_init()
    # demoProject项目初始化
    DemoProjectInit().init()
