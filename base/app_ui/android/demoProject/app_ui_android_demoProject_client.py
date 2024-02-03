#
# app_ui_android_demoProject_client.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2022-11-07T13:47:34.050Z+08:00
# @last-modified 2023-04-28T13:33:22.367Z+08:00
#

from appium import webdriver
from appium.options.common.base import AppiumOptions
from base.app_ui.android.demoProject.app_ui_android_demoProject_read_config import APP_UI_Android_DemoProject_Read_Config
from base.read_app_ui_config import Read_APP_UI_Config
from common.appium.app_operator import AppOperator
from common.file_tool import FileTool
from common.httpclient.do_request import DoRequest
from init.app_ui.android.demoProject.demoProjectInit import DemoProjectInit
import os

class APP_UI_Android_demoProject_Client(object):

    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,is_need_reset_app=False,is_need_kill_app=False):
        if self.__inited is None:
            self.__inited=True
            self.__is_first=True
            self.config = Read_APP_UI_Config().app_ui_config
            self.device_info=FileTool.readJsonFromFile('config/app_ui_tmp/'+str(os.getppid()))
            self.demoProject_config = APP_UI_Android_DemoProject_Read_Config('config/demoProject/%s'%self.device_info['app_ui_config']).config
            self.current_desired_capabilities = FileTool.readJsonFromFile('config/app_ui_tmp/' + str(os.getppid()) + '_current_desired_capabilities')
            self._appium_hub='http://'+self.device_info['server_ip']+':%s/wd/hub'%self.device_info['server_port']
            self._init(self.demoProject_config.init)
            self._delete_last_device_session(self.device_info['device_desc'])
            appiumOptions=AppiumOptions()
            for key in self.current_desired_capabilities.keys():
                appiumOptions.set_capability(key,self.current_desired_capabilities[key])
            self.driver = webdriver.Remote(self._appium_hub,options=appiumOptions)
            self._save_last_device_session(self.driver.session_id, self.device_info['device_desc'])
            self.app_operator = AppOperator(self.driver,self._appium_hub)

        if is_need_reset_app:
            # appium启动是非重置或者非第一次appium启动，则要进行重置
            if self.__is_first==False or self.noReset==True:
                self.app_operator.reset_app()
        elif is_need_kill_app:
            # appium启动是非重置或者非第一次appium启动，则要进行重启进程
            if self.__is_first==False or self.noReset==True:
                self.app_operator.start_activity('com.moji.mjweather','com.moji.mjweather.MainActivity')
    
        self.__is_first=False

    def _init(self,is_init=False):
        print('初始化android基础数据......')
        DemoProjectInit().init(is_init)
        print('初始化android基础数据完成......')

    def _save_last_device_session(self,session, device_desc):
        if not os.path.exists('config/app_ui_tmp'):
            os.mkdir('config/app_ui_tmp')
            with open('config/app_ui_tmp/%s_session' % device_desc, 'w') as f:
                f.write(session)
                f.close()

    def _delete_last_device_session(self,device_desc):
        if os.path.exists('config/app_ui_tmp/%s_session' % device_desc):
            with open('config/app_ui_tmp/%s_session' % device_desc, 'r') as f:
                last_session = f.read()
                last_session = last_session.strip()
                if last_session:
                    doRequest = DoRequest(self._appium_hub)
                    doRequest.setHeaders({'Content-Type': 'application/json'})
                    httpResponseResult = doRequest.delete('/session/' + last_session)
