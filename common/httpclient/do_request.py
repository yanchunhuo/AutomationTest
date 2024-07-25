#
# do_request.py
# @author yanchunhuo
# @description 
# @created 2018-01-19T22:10:09.163Z+08:00
# @last-modified 2024-07-25T10:36:52.431Z+08:00
# github https://github.com/yanchunhuo

from curlify2 import Curlify
from pojo.httpResponseResult import HttpResponseResult
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
import urllib
import requests
import ujson


class DoRequest(object):
    def __init__(self, url=None, encoding='utf-8', pool_connections=10, pool_maxsize=10, max_retries=2, timeout=30,
                 verify=True):
        self._url = url
        self._encoding = encoding
        self._headers = {}
        self._cookies = {}
        self._proxies = {}
        self._timeout = timeout
        self._verify = verify
        self._session = requests.session()
        httpAdapter = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=max_retries)
        self._session.mount('http://', httpAdapter)
        self._session.mount('https://', httpAdapter)
        self._curl_command = None
        self._response = None

    def get_url(self):
        return self._url

    def get_response(self):
        return self._response

    def setHeaders(self, headers):
        self._headers = headers

    def updateHeaders(self, headers):
        self._headers.update(headers)

    def removeHeader(self, key):
        self._headers.pop(key)

    def getHeaders(self):
        return self._headers

    def setCookies(self, cookies):
        self._cookies = cookies

    def updateCookies(self, cookies):
        self._cookies.update(cookies)

    def getCookies(self):
        return self._cookies

    def setTimeout(self, seconds):
        self._timeout = seconds

    def setProxies(self, proxies):
        self._proxies = proxies

    def setVerify(self, verify: bool = True):
        self._verify = verify

    def post_with_form(self, path, params=None, **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.post(url=url, data=params, headers=self._headers, cookies=self._cookies,
                                            timeout=self._timeout,
                                            proxies=self._proxies, verify=self._verify, **kwargs)
        return self._dealResponseResult(params=params)

    def post_with_json(self, path, params=None, **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.post(url=url, json=params, headers=self._headers, cookies=self._cookies,
                                            timeout=self._timeout,
                                            proxies=self._proxies, verify=self._verify, **kwargs)

        return self._dealResponseResult(params=params)

    def post_with_file(self, path, filePath, params=None, fileKey='file', **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        files = {fileKey: open(filePath, 'rb')}
        self._response = self._session.post(url=url, data=params, files=files, headers=self._headers,
                                            cookies=self._cookies,
                                            timeout=self._timeout, proxies=self._proxies, verify=self._verify, **kwargs)

        return self._dealResponseResult(params=params, files=files)

    def put(self, path, params=None, **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.put(url=url, data=params, headers=self._headers, cookies=self._cookies,
                                           timeout=self._timeout,
                                           proxies=self._proxies, verify=self._verify, **kwargs)
        return self._dealResponseResult(params=params)

    def get(self, path, params=None, **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.get(url=url, params=params, headers=self._headers, cookies=self._cookies,
                                           timeout=self._timeout,
                                           proxies=self._proxies, verify=self._verify, **kwargs)
        return self._dealResponseResult(params=params)

    def delete(self, path, **kwargs):
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.delete(url=url, headers=self._headers, cookies=self._cookies,
                                              timeout=self._timeout,
                                              proxies=self._proxies, verify=self._verify, **kwargs)
        return self._dealResponseResult()

    def getFile(self, path, storeFilePath, params=None, **kwargs):
        """
        下载文件
        :param path:
        :param storeFilePath:
        :param params:
        :return:
        """
        if not path.startswith('http'):
            url = self._url + path
        else:
            url = path
        self._response = self._session.get(url=url, params=params, headers=self._headers, cookies=self._cookies,
                                           timeout=self._timeout, proxies=self._proxies, verify=self._verify, **kwargs)
        httpResponseResult = HttpResponseResult()
        httpResponseResult.status_code = self._response.status_code
        httpResponseResult.headers = self._session.headers.__str__()
        self.updateCookies(self._session.cookies.get_dict())
        httpResponseResult.cookies = ujson.dumps(self.getCookies())
        with open(storeFilePath, "wb") as f:
            f.write(self._response.content)
        self._deal_curl_info(self._response, params=params)
        return httpResponseResult

    def _dealResponseResult(self, params=None, files=None):
        """
        将请求结果封装到HttpResponseResult
        :param r: requests请求响应
        :return:
        """
        self._response.encoding = self._encoding
        httpResponseResult = HttpResponseResult()
        httpResponseResult.status_code = self._response.status_code
        httpResponseResult.headers = self._response.headers.__str__()
        self.updateCookies(self._session.cookies.get_dict())
        httpResponseResult.cookies = ujson.dumps(self.getCookies())
        httpResponseResult.body = self._response.content.decode(self._encoding)
        self._deal_curl_info(self._response, params=params, files=files)
        return httpResponseResult

    def _deal_curl_info(self, response, params=None, files=None):
        try:
            self._curl_command = Curlify(response.request, compressed=True).to_curl()
        except UnicodeDecodeError as e:
            # return '无法转换为curl命令'
            prepared_request = response.request

            # 手动构建 cURL 命令
            self._curl_command = f"curl -X {prepared_request.method} '{prepared_request.url}'"
            for header, value in prepared_request.headers.items():
                self._curl_command += f" -H '{header}: {value}'"

            if files:
                for key, value in files.items():
                    self._curl_command += f" -F '{key}={value.name}'"

            if params:
                payload = urllib.parse.urlencode(params, doseq=True)
                self._curl_command += f" --data '{payload}'"
        self._curl_command = self._curl_command.encode('latin1').decode('unicode_escape')

    def get_curl_command(self, truncate=True):
        """
        获取请求的curl命令
        :param truncate:是否截断，默认是
        :return:
        """
        if truncate:
            if len(self._curl_command) > 5000:
                return self._curl_command[:5000] + '...太长了截断'
        return self._curl_command

    def changeUrl(self, url):
        self._url = url

    def closeSession(self):
        self._session.close()