#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from pojo.httpResponseResult import HttpResponseResult
from requests.adapters import HTTPAdapter
import requests
import ujson
class DoRequest(object):
    def __init__(self,url,encoding='utf-8',pool_connections=10,pool_maxsize=10, max_retries=2,timeout=30,verify=True):
        self._url=url
        self._encoding=encoding
        self._headers = {}
        self._cookies = {}
        self._proxies={}
        self._timeout=timeout
        self._verify=verify
        self._session=requests.session()
        httpAdapter=HTTPAdapter(pool_connections=pool_connections,pool_maxsize=pool_maxsize,max_retries=max_retries)
        self._session.mount('http://',httpAdapter)
        self._session.mount('https://', httpAdapter)

    def setHeaders(self, headers):
        self._headers = headers

    def updateHeaders(self, headers):
        self._headers.update(headers)
    
    def removeHeader(self,key):
        self._headers.pop(key)

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
        
    def setVerify(self,verify:bool=True):
        self._verify=verify

    def post_with_form(self,path,params=None,**kwargs):
        r=self._session.post(self._url+path,data=params,headers=self._headers,cookies=self._cookies,timeout=self._timeout,
                        proxies=self._proxies,verify=self._verify,**kwargs)
        return self._dealResponseResult(r)

    def post_with_file(self,path,filePath,params=None,fileKey='file',**kwargs):
        files = {fileKey: open(filePath, 'rb')}
        r = self._session.post(self._url+path, data=params, files=files,headers=self._headers, cookies=self._cookies,
                          timeout=self._timeout,proxies=self._proxies,verify=self._verify,**kwargs)
        return self._dealResponseResult(r)

    def put(self,path,params=None,**kwargs):
        r=self._session.put(self._url+path,data=params,headers=self._headers,cookies=self._cookies,timeout=self._timeout,
                        proxies=self._proxies,verify=self._verify,**kwargs)
        return self._dealResponseResult(r)

    def get(self,path,params=None,**kwargs):
        r = self._session.get(self._url+path, params=params, headers=self._headers, cookies=self._cookies, timeout=self._timeout,
                          proxies=self._proxies,verify=self._verify,**kwargs)
        return self._dealResponseResult(r)

    def delete(self,path,**kwargs):
        r = self._session.delete(self._url+path,headers=self._headers, cookies=self._cookies, timeout=self._timeout,
                          proxies=self._proxies,verify=self._verify,**kwargs)
        return self._dealResponseResult(r)

    def getFile(self,path,storeFilePath,params=None,**kwargs):
        """
        下载文件
        :param path:
        :param storeFilePath:
        :param params:
        :return:
        """
        r = self._session.get(self._url + path, params=params, headers=self._headers, cookies=self._cookies,
                              timeout=self._timeout, proxies=self._proxies, verify=self._verify, **kwargs)
        httpResponseResult = HttpResponseResult()
        httpResponseResult.status_code=r.status_code
        httpResponseResult.headers=self._session.headers.__str__()
        self.updateCookies(self._session.cookies.get_dict())
        httpResponseResult.cookies=ujson.dumps(self.getCookies())
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
        self.updateCookies(self._session.cookies.get_dict())
        httpResponseResult.cookies=ujson.dumps(self.getCookies())
        httpResponseResult.body=r.content.decode(self._encoding)
        return httpResponseResult

    def changeUrl(self,url):
        self._url=url

    def closeSession(self):
        self._session.close()