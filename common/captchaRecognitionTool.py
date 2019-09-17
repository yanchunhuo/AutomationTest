#-*- coding:utf8 -*-
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
