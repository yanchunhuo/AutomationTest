# -*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from common.file_tool import FileTool
from pojo.api.demoProject.demoProjectConfig import DemoProjectConfig
import configparser as ConfigParser
import os

class API_DemoProject_Read_Config(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,config_file_path:str=None,env:str=None):
        """优先取传参配置文件，再取传参环境，最后去运行指定的环境

        Args:
            config_file_path (str, optional): 如果指定该参数，env参数被忽略. Defaults to None.
            env (str, optional): _description_. Defaults to None.
        """
        if self.__inited is None:
            if config_file_path is None:
                if env is None:
                    if os.path.exists('config/tmp/env.json'):
                        env_info=FileTool.readJsonFromFile('config/tmp/env.json')
                        env=env_info['env']
                    else:
                        env='test'
                if env.lower()=='test':
                    config_file_path='config/demoProject/api_demoProject_test.conf'
                elif env.lower()=='release':
                    config_file_path='config/demoProject/api_demoProject_release.conf'
            self.config=self._readConfig(config_file_path)
            self.env=env
            
            self.__inited=True

    def _readConfig(self,configFile):
        config = ConfigParser.ConfigParser()
        config.read(configFile,encoding='utf-8')
        demoProjectConfig=DemoProjectConfig()
        demoProjectConfig.url=config.get('servers','url')
        demoProjectConfig.init=config.get('isInit','init')
        return demoProjectConfig