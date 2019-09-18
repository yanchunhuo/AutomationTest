#-*- coding:utf-8 -*-
from page_objects.web_ui.demoProject.elements.loginPageElements import LoginPageElements
from page_objects.web_ui.demoProject.pages.indexPage import IndexPage
class LoginPage:
    def __init__(self,browserOperator):
        self._browserOperator=browserOperator
        self._loginPageElements=LoginPageElements()
        self._browserOperator.explicit_wait_page_title(self._loginPageElements.title)
        self._browserOperator.get_screenshot('loginPage')

    def _send_login_info(self,username,password):
        self._browserOperator.sendText(self._loginPageElements.usernameInput, username)
        self._browserOperator.sendText(self._loginPageElements.passwordInput, password)

    def _login_submit(self):
        self._browserOperator.click(self._loginPageElements.loginBtn)

    def login_success(self,username,password):
        self._send_login_info(username,password)
        self._login_submit()
        self._browserOperator.get_screenshot('loginSuccess')
        return IndexPage(self._browserOperator)

    def login_fail(self,username,password):
        self._send_login_info(username, password)
        self._login_submit()
        self._browserOperator.get_screenshot('loginFail')

    def getElements(self):
        return self._loginPageElements