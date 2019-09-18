# -*- coding:utf-8 -*-
class DemoProjectConfig:
    def __init__(self):
        self.platformName = None
        self.automationName = None
        self.platformVersion = None
        self.deviceName = None
        self.appActivity = None
        self.appPackage = None
        self.app = None
        self.init = None

    def get_desired_capabilities(self):
        desired_capabilities={}
        desired_capabilities.update({'platformName':self.platformName})
        if self.automationName:
            desired_capabilities.update({'automationName':self.automationName})
        desired_capabilities.update({'platformVersion':self.platformVersion})
        desired_capabilities.update({'deviceName':self.deviceName})
        if self.appActivity and self.appPackage:
            desired_capabilities.update({'appActivity':self.appActivity})
            desired_capabilities.update({'appPackage':self.appPackage})
        if self.app:
            desired_capabilities.update({'app':self.app})
        return desired_capabilities