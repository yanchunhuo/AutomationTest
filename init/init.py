#-*- coding:utf8 -*-
from init.demoProject.demoProjectInit import DemoProjectInit
import configparser as ConfigParser

def init():
    """
    初始化必要的数据
    :return:
    """
    config = ConfigParser.ConfigParser()
    config.read('config/init.conf',encoding='utf-8')

    #初始化demoProject项目基础数据
    if 1==int(config.get('isInit','demoProject')):
        DemoProjectInit().init()