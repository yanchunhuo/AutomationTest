#-*- coding:utf8 -*-

class HttpResponseResult:
    def __init__(self):
        self._status_code=None
        self._body=None
        self._cookies=None
        self._headers=None

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self,status_code):
        self._status_code=status_code

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self,body):
        self._body=body

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self,cookies):
        self._cookies=cookies

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self,headers):
        self._headers=headers