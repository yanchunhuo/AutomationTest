# -*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.api.demoProject.api_demoProject_read_config import API_DemoProject_Read_Config
from base.api.demoProject.api_demoProject_db_clients import API_DemoProject_DB_Clients
from common.httpclient.doRequest import DoRequest

class API_DemoProject_Client(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,config_file_path:str=None,env:str=None):
        if self.__inited is None:
            self.demoProjectConfig=API_DemoProject_Read_Config(config_file_path,env).config
            self.demoProjectDBClients=API_DemoProject_DB_Clients()
            self.doRequest=DoRequest(self.demoProjectConfig.url)

            self.__inited=True
