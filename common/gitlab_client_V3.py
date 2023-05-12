# gitlab_client_V3.py
# @author yanchunhuo
# @description 
# @created 2021-04-13T10:59:58.738Z+08:00
# @last-modified 2023-05-12T11:10:42.216Z+08:00
# github https://github.com/yanchunhuo
from common.httpclient.doRequest import DoRequest
from urllib.parse import urljoin
import ujson


"""
本工具支持gitlab的API版本为V3
"""
class GitlabClientV3:
    def __init__(self,url:str,username:str,password:str):
        self.url=url
        self.username=username
        self.password=password
        self.url=urljoin(self.url,'/api/v3')
        self.doRequest=DoRequest(self.url)
        self.private_token=self._get_private_token()
        self._path_private_token='?private_token=%s'%self.private_token

    def _login(self):
        httpResponseResult=self.doRequest.post_with_form('/session?login=%s&password=%s'%(self.username,self.password))
        return httpResponseResult

    def _get_private_token(self):
        user_info=self._login().body
        user_info=ujson.loads(user_info)
        return user_info['private_token']

    def get_user(self):
        return ujson.loads(self._login().body)

    def get_projects(self,page:int=1,per_page:int=100):
        params={'page':1,'per_page':100}
        httpResponseResult=self.doRequest.get('/projects%s'%self._path_private_token,params=params)
        return ujson.loads(httpResponseResult.body)

    def _get_project_id(self,project_name:str):
        projects=self.get_projects()
        for project_info in projects:
            if project_info['name']==project_name.strip():
                return project_info['id']

    def get_project_tree(self,project_name:str):
        project_id=self._get_project_id(project_name)
        httpResponsResult=self.doRequest.get('/projects/%s/repository/tree%s'%(project_id,self._path_private_token))
        return ujson.loads(httpResponsResult.body)

    def get_project_file(self,project_name,ref,file_path):
        """
        @param project_name:
        @param ref: 分支名、tag名、commit
        @param file_path:
        @return:
        """
        project_id=self._get_project_id(project_name)
        params={'file_path':file_path,'ref':ref}
        httpResponsResult=self.doRequest.get('/projects/%s/repository/files%s'%(project_id,self._path_private_token),params=params)
        return ujson.loads(httpResponsResult.body)

    def update_project_file(self,project_name:str,branch_name:str,file_path:str,content:str,commit_message:str):
        """
        @param project_name:
        @param branch_name:
        @param file_path:
        @param content:
        @param commit_message:
        @return:
        """
        project_id=self._get_project_id(project_name)
        params={'file_path':file_path,'branch_name':branch_name,'content':content,'commit_message':commit_message}
        httpResponsResult=self.doRequest.put('/projects/%s/repository/files%s'%(project_id,self._path_private_token),params=params)
        return ujson.loads(httpResponsResult.body)

