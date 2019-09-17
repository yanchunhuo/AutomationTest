#!-*- coding:utf8 -*-
import re

class NumberTool:

    @classmethod
    def isPhoneAvailable(cls,mobile):
        """
        判断手机号是否合法
        :param mobile:
        :return:
        """
        mobile=str(mobile)
        regular=re.compile('^1[3578]\d{9}$|^14[56789]\d{8}$')
        if regular.match(mobile):
            return True
        else:
            return False