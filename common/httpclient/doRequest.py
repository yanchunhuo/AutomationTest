#-*- coding:utf8 -*-
import requests
from pojo.httpResponseResult import HttpResponseResult

class DoRequest(object):
    def __init__(self,url,encoding='utf-8'):
        self._url=url
        self._encoding=encoding
        self._headers = {}
        self._cookies = {}
        self._proxies={}
        self._timeout=120
        self._session=requests.session()

    def setHeaders(self, headers):
        self._headers = headers

    def updateHeaders(self, headers):
        self._headers.update(headers)

    def getHeaders(self):
        return self._headers

    def setCookies(self, cookies):
        self._cookies = cookies

    def updateCookies(self, cookies):
        self._cookies.update(cookies)

    def getCookies(self):
        return self._cookies

    def setTimeout(self,seconds):
        self._timeout=seconds

    def setProxies(self,proxies):
        self._proxies=proxies

    def post_with_form(self,path,params=None,**kwargs):
        r=self._session.post(self._url+path,data=params,headers=self._headers,cookies=self._cookies,timeout=self._timeout,
                        proxies=self._proxies,**kwargs)
        return self._dealResponseResult(r)


    def post_with_file(self,path,filePath,params=None,fileKey='file',**kwargs):
        files = {fileKey: open(filePath, 'rb')}
        r = self._session.post(self._url+path, data=params, files=files,headers=self._headers, cookies=self._cookies,
                          timeout=self._timeout,proxies=self._proxies,**kwargs)
        return self._dealResponseResult(r)

    def get(self,path,params=None,**kwargs):
        r = self._session.get(self._url+path, params=params, headers=self._headers, cookies=self._cookies, timeout=self._timeout,
                          proxies=self._proxies,**kwargs)
        return self._dealResponseResult(r)

    def delete(self,path,**kwargs):
        r = self._session.delete(self._url+path,headers=self._headers, cookies=self._cookies, timeout=self._timeout,
                          proxies=self._proxies,**kwargs)
        return self._dealResponseResult(r)

    def getFile(self,path,storeFilePath,params=None,**kwargs):
        """
        下载文件
        :param path:
        :param storeFilePath:
        :param params:
        :return:
        """
        r=requests.get(self._url+path,params=params,headers=self._headers, cookies=self._cookies, timeout=self._timeout,
                       proxies=self._proxies,**kwargs)
        httpResponseResult=HttpResponseResult()
        httpResponseResult.status_code=r.status_code
        httpResponseResult.headers=self._session.headers.__str__()
        httpResponseResult.cookies=self._session.cookies.__str__()
        with open(storeFilePath,"wb") as f:
            f.write(r.content)
        return httpResponseResult

    def _dealResponseResult(self,r):
        """
        将请求结果封装到HttpResponseResult
        :param r: requests请求响应
        :return:
        """
        r.encoding=self._encoding
        httpResponseResult=HttpResponseResult()
        httpResponseResult.status_code=r.status_code
        httpResponseResult.headers=r.headers.__str__()
        httpResponseResult.cookies=r.cookies.__str__()
        httpResponseResult.body=r.content.decode(self._encoding)
        return httpResponseResult

    def changeUrl(self,url):
        self._url=url

    def closeSession(self):
        self._session.close()
