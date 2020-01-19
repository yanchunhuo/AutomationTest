# @Author  : yanchunhuo
# @Time    : 2020/1/19 14:35
from common.network import Network
from pojo.httpserver_config import HttpServer_Config
import configparser as ConfigParser

class Read_Http_Server_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.httpserver_config=self._readConfig('config/httpserver.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile,encoding='utf-8')
        httpserver_config = HttpServer_Config()
        httpserver_config.local_ip=configParser.get('baseInfo','local_ip').strip()
        if not httpserver_config.local_ip:
            httpserver_config.local_ip=Network.get_local_ip()
        httpserver_config.httpserver_port=configParser.get('baseInfo','httpserver_port').strip()
        if not httpserver_config.httpserver_port:
            httpserver_config.httpserver_port=str(8000)
        return httpserver_config