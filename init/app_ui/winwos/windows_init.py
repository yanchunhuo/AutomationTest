#-*- coding:utf8 -*-
from init.java.java_maven_init import java_maven_init

def windows_init():
    """
    初始化Windows必要的数据
    :return:
    """
    # 初始化图像识别tess4j依赖的libs
    java_maven_init()