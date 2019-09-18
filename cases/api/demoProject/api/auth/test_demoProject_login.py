#-*- coding:utf8 -*-
from assertpy import assert_that
from base.api.demoProject.api_demoProject_client import API_DemoProject_Client
import pytest

class TestLogin:

    def setup_class(self):
        self._api_demoProject_client=API_DemoProject_Client()
        self._login_path='/horizon/auth/login/'

    @pytest.fixture
    def fixture_test_success_login(self):
        #setup
        print('this is a setup')
        #teardown
        yield self.fixture_test_success_login
        print('this is a teardown')

    def generateParams(self,csrfmiddlewaretoken,username,password,fake_email,fake_password):
        params={}
        params.update({"csrfmiddlewaretoken":csrfmiddlewaretoken})
        params.update({"username": username})
        params.update({"password": password})
        params.update({"fake_email": fake_email})
        params.update({"fake_password": fake_password})
        return params

    def test_success_login(self,fixture_test_success_login):
        params=self.generateParams(self._api_demoProject_client.csrftoken,'admin','admin','admin','admin')
        httpResponseResult=self._api_demoProject_client.doRequest.post_with_form(self._login_path,params=params)
        status_code=httpResponseResult.status_code
        body=httpResponseResult.body
        assert_that(status_code).is_equal_to(200)
        assert_that(body).contains('admin')

    def test_fail_login(self):
        params=self.generateParams(self._api_demoProject_client.csrftoken,'admin','admin1','admin','admin1')
        httpResponseResult=self._api_demoProject_client.doRequest.post_with_form(self._login_path,params=params)
        status_code=httpResponseResult.status_code
        body=httpResponseResult.body
        assert_that(status_code).is_equal_to(403)
        assert_that(body).contains('admin')

    @pytest.mark.skip(reason=u'空密码前端做校验')
    def test_empty_password_login(self):
        params=self.generateParams(self._api_demoProject_client.csrftoken,'admin','','admin','')
        httpResponseResult=self._api_demoProject_client.doRequest.post_with_form(self._login_path,params=params)
        status_code=httpResponseResult.status_code
        body=httpResponseResult.body
        assert_that(status_code).is_equal_to(403)
        assert_that(body).contains('admin')

    fail_data=[('11111','1111'),('admin',''),('',''),(u'中文用户名',u'中文密码')]
    @pytest.mark.parametrize('username,password',fail_data)
    def test_with_params_fail_login(self,username,password):
        params = self.generateParams(self._api_demoProject_client.csrftoken, username, password, username, password)
        httpResponseResult = self._api_demoProject_client.doRequest.post_with_form(self._login_path, params=params)
        status_code = httpResponseResult.status_code
        body=httpResponseResult.body
        assert_that(status_code).is_equal_to(403)
        assert_that(body).contains('admin')

    def teardown_class(self):
        pass

