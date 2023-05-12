# gitlab_client.py
# @author yanchunhuo
# @description 
# @created 2021-04-25T15:04:47.417Z+08:00
# @last-modified 2023-05-12T11:10:52.530Z+08:00
# github https://github.com/yanchunhuo
from common.httpclient.doRequest import DoRequest
from urllib.parse import urljoin
import ujson

"""
本工具支持gitlab的API版本为V4
"""
class GitlabClient:
    def __init__(self,url:str,access_token:str):
        self.url=url
        self.access_token=access_token
        self.url=urljoin(self.url,'/api/v4')
        self.doRequest=DoRequest(self.url)
        self.doRequest.updateHeaders({'PRIVATE-TOKEN':self.access_token})

    def get_projects(self,page:int=1,per_page:int=100,search='',simple=True):
        params={'page':page,'per_page':per_page}
        httpResponseResult=self.doRequest.get('/projects?simple=%s&search=%s'%(simple,search),params=params)
        return ujson.loads(httpResponseResult.body)

    def _get_project_id(self,project_name:str):
        projects=self.get_projects(search=project_name)
        for project_info in projects:
            if project_info['name']==project_name.strip():
                return project_info['id']

    def get_project_file(self,project_name,ref,file_path):
        """
        @param project_name:
        @param ref: 分支名、tag名、commit
        @param file_path:
        @return:
        """
        project_id=self._get_project_id(project_name)
        params={'ref':ref}
        httpResponsResult=self.doRequest.get('/projects/%s/repository/files/%s'%(project_id,file_path),params=params)
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
        params={'branch':branch_name,'content':content,'commit_message':commit_message}
        httpResponsResult=self.doRequest.put('/projects/%s/repository/files/%s'%(project_id,file_path),params=params)
        return ujson.loads(httpResponsResult.body)

