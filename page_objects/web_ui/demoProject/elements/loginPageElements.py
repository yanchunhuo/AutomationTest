#-*- coding:utf8 -*-
from page_objects.web_ui.locator_type import Locator_Type
from page_objects.createElement import CreateElement
from page_objects.web_ui.wait_type import Wait_Type as Wait_By
class LoginPageElements:
    def __init__(self):
        self.path = '/cloud/auth/login/?next=/cloud/'
        self.title = CreateElement.create(None,None,None,Wait_By.TITLE_IS,'登录 - 百悟云')
        self.usernameInput = CreateElement.create(Locator_Type.ID,'id_username',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.passwordInput = CreateElement.create(Locator_Type.ID,'id_password',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.loginBtn = CreateElement.create(Locator_Type.ID,'loginBtn',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)

        self.loginWrongUsernameAndPassword_tip = CreateElement.create(Locator_Type.CSS_SELECTOR,
                                                                         'div.alert:nth-child(3) > p:nth-child(1)',
                                                                         '用户名或密码不正确',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.loginEmptyUsername_tip = CreateElement.create(Locator_Type.CSS_SELECTOR,
                                                              '.help-block',
                                                              '这个字段是必填项。',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.loginEmptyPassword_tip = CreateElement.create(Locator_Type.CSS_SELECTOR,
                                                              '.help-block',
                                                              '这个字段是必填项。',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.loginEmptyUsernameAndPassword_username_tip = CreateElement.create(Locator_Type.CSS_SELECTOR,
                                                         'div.form-group:nth-child(4) > span:nth-child(4)',
                                                         '这个字段是必填项。',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
        self.loginEmptyUsernameAndPassword_password_tip = CreateElement.create(Locator_Type.CSS_SELECTOR,
                                                           'div.form-group:nth-child(7) > span:nth-child(4)',
                                                           '这个字段是必填项。',None,Wait_By.PRESENCE_OF_ELEMENT_LOCATED)
