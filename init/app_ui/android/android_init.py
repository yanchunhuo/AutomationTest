#-*- coding:utf8 -*-
from init.tess4j.tess4j_maven_init import tess4j_maven_init
from init.app_ui.android.demoProject.demoProjectInit import DemoProjectInit

def android_init():
    """
    初始化android项目必要的数据
    :return:
    """
    # 初始化图像识别tess4j依赖的libs
    tess4j_maven_init()
    # demoProject项目初始化
    DemoProjectInit().init()
