# -*- coding:utf8 -*-
from base.api.demoProject.api_demoProject_read_config import API_DemoProject_Read_Config
from base.api.demoProject.api_demoProject_db_clients import API_DemoProject_DB_Clients
from common.httpclient.doRequest import DoRequest
from common.strTool import StrTool

class API_DemoProject_Client(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.demoProjectConfig=API_DemoProject_Read_Config().config
            self.demoProjectDBClients=API_DemoProject_DB_Clients()
            self.doRequest=DoRequest(self.demoProjectConfig.url)
            self.csrftoken=self._initCsrftoken()

            self.__inited=True

    def _initCsrftoken(self):
        # 测试接口如果都需要先授权，可以在再次操作，将授权信息放到httpclient的headers或者cookies
        httpResponseResult = self.doRequest.get("/horizon/auth/login/?next=/horizon/")
        cookies = httpResponseResult.cookies
        csrftoken = StrTool.getStringWithLBRB(cookies, 'csrftoken=', ' for')
        return csrftoken