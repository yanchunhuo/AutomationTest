# -*- coding:utf8 -*-
from assertpy import assert_that
from base.web_ui.demoProject.web_ui_demoProject_client import WEB_UI_DemoProject_Client
from page_objects.web_ui.demoProject.pages.loginPage import LoginPage
import pytest
class TestLogin:

    def setup_class(self):
        self.demoProjectClient=WEB_UI_DemoProject_Client()
        self.loginPage=LoginPage(self.demoProjectClient.browserOperator)

    @pytest.fixture
    def fixture_test_login_success(self):
        yield self.fixture_test_login_success
        self.indexPage.click_user()
        self.indexPage.click_user_logout()

    def test_login_success(self,fixture_test_login_success):
        self.indexPage=self.loginPage.login_success(self.demoProjectClient.demoProjectConfig.normal_username,self.demoProjectClient.demoProjectConfig.normal_password)
        assert_that(self.demoProjectClient.browserOperator.getTitle()).is_equal_to(self.indexPage.getElements().title.wait_expected_value)

    def test_empty_username_and_empty_password(self):
        self.loginPage.login_fail('', '')
        assert_that(self.demoProjectClient.browserOperator.getText(
            self.loginPage.getElements().loginEmptyUsernameAndPassword_password_tip)).is_equal_to(
            self.loginPage.getElements().loginEmptyUsernameAndPassword_password_tip.expected_value)
        assert_that(self.demoProjectClient.browserOperator.getText(
            self.loginPage.getElements().loginEmptyUsernameAndPassword_username_tip)).is_equal_to(
            self.loginPage.getElements().loginEmptyUsernameAndPassword_username_tip.expected_value)

    def test_empty_username(self):
        self.loginPage.login_fail('','123456')
        assert_that(self.demoProjectClient.browserOperator.getText(
            self.loginPage.getElements().loginEmptyUsername_tip)).is_equal_to(
            self.loginPage.getElements().loginEmptyUsername_tip.expected_value)

    def test_empty_password(self):
        self.loginPage.login_fail('admin', '')
        assert_that(self.demoProjectClient.browserOperator.getText(
            self.loginPage.getElements().loginEmptyPassword_tip)).is_equal_to(
            self.loginPage.getElements().loginEmptyPassword_tip.expected_value)

    def teardown_class(self):
        self.demoProjectClient.browserOperator.close()