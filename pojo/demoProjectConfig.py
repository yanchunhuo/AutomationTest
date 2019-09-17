#-*- coding:utf8 -*-
class DemoProjectConfig:
    def __init__(self):
        self._url=None
        self._adminUser=None
        self._adminUserPassword = None
        self._normalUser=None
        self._normalUserPassword=None
        self._closeUser=None
        self._closeUserPassword=None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self,url):
        self._url=url

    @property
    def adminUser(self):
        return self._adminUser

    @adminUser.setter
    def adminUser(self,adminUser):
        self._adminUser=adminUser

    @property
    def adminUserPassword(self):
        return self._adminUserPassword

    @adminUserPassword.setter
    def adminUserPassword(self,adminUserPassword):
        self._adminUserPassword=adminUserPassword

    @property
    def normalUser(self):
        return self._normalUser

    @normalUser.setter
    def normalUser(self,normalUser):
        self._normalUser=normalUser

    @property
    def normalUserPassword(self):
        return self._normalUserPassword

    @normalUserPassword.setter
    def normalUserPassword(self,normalUserPassword):
        self._normalUserPassword=normalUserPassword

    @property
    def closeUser(self):
        return self._closeUser

    @closeUser.setter
    def closeUser(self,closeUser):
        self._closeUser=closeUser

    @property
    def closeUserPassword(self):
        return self._closeUserPassword

    @closeUserPassword.setter
    def closeUserPassword(self,closeUserPassword):
        self._closeUserPassword=closeUserPassword

