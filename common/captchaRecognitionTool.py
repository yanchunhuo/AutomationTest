#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import jpype
from common.java.javaTools import StartJpypeJVM
class CaptchaRecognitionTool:

    @classmethod
    def captchaRecognition(cls,filePath,language='eng'):
        """

        :param filePath: 图片验证码
        :param language: eng:英文,chi_sim:中文
        :return:
        """

        # 启动jvm......'
        StartJpypeJVM()
        CaptchaRecognition = jpype.JClass('com.ocr.CaptchaRecognition')
        captchaRecognition = CaptchaRecognition('common/java/lib/tess4j/tessdata/')
        captcha = captchaRecognition.captchaRecognitionWithFile(filePath,language)
        return captcha
