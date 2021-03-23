# @Author  : yanchunhuo
# @Time    : 2020/7/15 17:30
# github https://github.com/yanchunhuo
from common.network import Network
from pojo.mitmproxy_config import Mitmproxy_Config
import configparser as ConfigParser

class Read_Mitmproxy_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            self.mitmproxy_config=self._readConfig('config/mitmproxy.conf')
            self.__inited=True

    def _readConfig(self, configFile):
        configParser = ConfigParser.ConfigParser()
        configParser.read(configFile,encoding='utf-8')
        mitmproxy_config = Mitmproxy_Config()
        mitmproxy_config.proxy_port=configParser.get('baseInfo','proxy_port').strip()
        ssl_insecure=configParser.get('baseInfo','ssl_insecure').strip()
        if 'true' == ssl_insecure.lower():
            ssl_insecure=True
        else:
            ssl_insecure=False
        mitmproxy_config.ssl_insecure=ssl_insecure
        if not mitmproxy_config.proxy_port:
            mitmproxy_config.proxy_port=str(8080)
        return mitmproxy_config