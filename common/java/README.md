# [Python调用Java代码说明]()

# [注意点]()
* 在Python线程中如有调用java相关代码时,需要在Python线程体(run方法)中调用jpype.attachThreadToJVM()

## 一、tess4j
* 1、图片验证码识别

```python
import jpype
CaptchaRecognition = jpype.JClass('com.ocr.CaptchaRecognition')
captchaRecognition = CaptchaRecognition('common/java/lib/tess4j/tessdata/')
captcha = captchaRecognition.captchaRecognitionWithFile("filePath","language")
```