# @Author  : yanchunhuo
# @Time    : 2020/7/21 10:24
# github https://github.com/yanchunhuo
from common.httpclient.doRequest import DoRequest
import ujson

class DisconfClient:
    def __init__(self,url:str,is_verify_ssl_cer=True):
        self.url=url
        self.doRequest=DoRequest(self.url)
        self.doRequest.setVerify(is_verify_ssl_cer)

    def login(self,username:str,password:str):
        params = {'name': username, 'password': password, 'remember': '1'}
        httpResponseResult=self.doRequest.post_with_form('/api/account/signin',params)
        return ujson.loads(httpResponseResult.body)

    def get_app_list(self):
        httpResponseResult=self.doRequest.get('/api/app/list')
        app_list=ujson.loads(httpResponseResult.body)
        app_list=app_list['page']['result']
        return app_list

    def get_app_id(self,app_name:str):
        app_list=self.get_app_list()
        for app_info in app_list:
            if app_info['name']==app_name:
                return app_info['id']

    def get_env_list(self):
        httpResponseResult = self.doRequest.get('/api/env/list')
        env_list=ujson.loads(httpResponseResult.body)
        env_list=env_list['page']['result']
        return env_list

    def get_env_id(self,env_name:str):
        env_list=self.get_env_list()
        for env_info in env_list:
            if env_info['name']==env_name:
                return env_info['id']

    def get_version_list(self,app_id:int,env_id:int):
        params={'appId':app_id,'envid':env_id}
        httpResponseResult = self.doRequest.get('/api/web/config/versionlist',params)
        version_list=ujson.loads(httpResponseResult.body)
        version_list=version_list['page']['result']
        return version_list

    def get_config_list(self, app_id: int, env_id: int, version: str, pageSize: int = 50, pageNo: int = 1):
        params = {'appId': app_id, 'envId': env_id, 'version': version, "page.pageSize": pageSize,"page.pageNo": pageNo}
        httpResponseResult = self.doRequest.get('/api/web/config/list',params)
        config_list=ujson.loads(httpResponseResult.body)
        config_list=config_list['page']['result']
        return config_list

    def get_config_id(self,app_name:str,env_name:str,version:str,config_name:str):
        now_page=1
        # 最多从500个文件获取
        while(not now_page>10):
            config_list = self.get_config_list(self.get_app_id(app_name), self.get_env_id(env_name), version,
                                               pageSize=50, pageNo=now_page)
            for config_info in config_list:
                if config_info['key']==config_name:
                    return config_info['configId']
            now_page+=1

    def get_config_info(self,config_id:int):
        httpResponseResult = self.doRequest.get('/api/web/config/%s'%config_id)
        config_info=ujson.loads(httpResponseResult.body)
        config_info=config_info['result']['value']
        return config_info

    def update_config_info(self,config_id:int,content:str):
        params={'fileContent':content}
        httpResponseResult = self.doRequest.put('/api/web/config/filetext/%s' % config_id,params)
        config_info = ujson.loads(httpResponseResult.body)
        return config_info

