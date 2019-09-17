# -*- coding:utf-8 -*-
from base.demoProject.demoProjectReadConfig import DemoProjectReadConfig


class DemoProjectDBClients(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self._demoProjectConfig = DemoProjectReadConfig().config
            # self.mysqlclient=MysqlClient('host','port','username','password','dbname')
            # self.oracleclient = OracleClient('host', 'port', 'username', 'password', 'dbname')
            self.__inited=True
