#!-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
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