#-*- coding:utf8 -*-
from base.read_web_ui_config import Read_WEB_UI_Config
from common.captchaRecognitionTool import CaptchaRecognitionTool
from common.dateTimeTool import DateTimeTool
from pojo.elementInfo import ElementInfo
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from page_objects.web_ui.wait_type import Wait_Type  as Wait_By
from PIL import Image
import allure
import os

class BrowserOperator:
    """
    类中的element参数可以有selenium.webdriver.remote.webelement.WebElement和pojo.elementInfo.ElementInfo类型
    """

    def __init__(self,driver):
        self._config = Read_WEB_UI_Config().web_ui_config
        self._driver=driver

    def _change_element_to_webElement_type(self,element,highlight_seconds=5):
        if isinstance(element, ElementInfo):
            webElement=self.getElement(element,highlight_seconds)
        elif isinstance(element,WebElement):
            webElement=element
        else:
            return None
        return webElement

    def get(self,url):
        self._driver.get(url)

    def get_current_url(self):
        return self._driver.current_url

    def getTitle(self):
        return self._driver.title

    def getText(self,element,highlight_seconds=5):
        webElement=self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            return webElement.text

    def click(self,element,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement.click()

    def submit(self,element,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement.submit()

    def sendText(self,element,text,highlight_seconds=5):
        text=text
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement.clear()
            webElement.send_keys(text)

    def send_keys(self,element,keys,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement.send_keys(keys)

    def is_displayed(self,element,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            flag=webElement.is_displayed()
            return flag

    def is_enabled(self,element,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            flag = webElement.is_enabled()
            return flag

    def is_selected(self,element,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            flag = webElement.is_selected()
            return flag

    def select_dropDownBox_by_value(self,element,value,highlight_seconds=5):
        """
        适用单选下拉框
        :param element:
        :param value:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.select_by_value(value)

    def select_dropDownBox_by_text(self,element,text,highlight_seconds=5):
        """
        适用单选下拉框
        :param element:
        :param text:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.select_by_visible_text(text)

    def select_dropDownBox_by_index(self,element,index,highlight_seconds=5):
        """
        适用单选下拉框,下标从0开始
        :param element:
        :param index:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.select_by_index(index)

    def select_dropDownBox_by_values(self,element,values,highlight_seconds=5):
        """
        适用多选下拉框
        :param element:
        :param values:以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.deselect_all()
            for value in values:
                webElement.select_by_value(value)

    def select_dropDownBox_by_texts(self,element,texts,highlight_seconds=5):
        """
        适用多选下拉框
        :param element:
        :param texts:以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.deselect_all()
            for text in texts:
                webElement.select_by_visible_text(text)

    def select_dropDownBox_by_indexs(self,element,indexs,highlight_seconds=5):
        """
        适用多选下拉框，下标从0开始
        :param element:
        :param indexs: 以数组传参
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement=Select(webElement)
            webElement.deselect_all()
            for index in indexs:
                webElement.select_by_index(index)

    def switch_to_window(self,window_name):
        self._driver.switch_to.window(window_name)

    def switch_to_frame(self,frame_name):
        self._driver.switch_to.frame(frame_name)

    def switch_to_parent_frame(self):
        self._driver.switch_to.parent_frame()

    def page_forward(self):
        self._driver.forward()

    def pag_back(self):
        self._driver.back()

    def dismiss_alert(self):
        alert=self._driver.switch_to.alert
        alert.dismiss()

    def accept_alert(self):
        alert=self._driver.switch_to.alert
        alert.accept()

    def get_alert_text(self):
        alert=self._driver.switch_to.alert
        return alert.text

    def get_screenshot(self,fileName):
        fileName=DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_')+fileName
        allure.attach(name=fileName,body=self._driver.get_screenshot_as_png(),attachment_type=allure.attachment_type.PNG)

    def refresh(self):
        self._driver.refresh()

    def uploadFile(self,element,filePath,highlight_seconds=5):
        """
        适用于元素为input且type="file"的文件上传
        :param element:
        :param filePath:
        :return:
        """
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            webElement.send_keys(os.path.abspath(filePath))

    def get_property(self,element,property_name,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            return webElement.get_property(property_name)

    def get_attribute(self,element,attribute_name,highlight_seconds=5):
        webElement = self._change_element_to_webElement_type(element,highlight_seconds)
        if webElement:
            return webElement.get_attribute(attribute_name)

    def get_element_outer_html(self,element):
        return self.get_attribute(element,'outerHTML')

    def get_element_inner_html(self, element):
        return self.get_attribute(element,'innerHTML')

    def get_page_source(self):
        return self._driver.page_source

    def get_captcha(self,element,language='eng',highlight_seconds=0):
        """
        识别图片验证码
        :param element: 验证码图片元素
        :param language: eng:英文,chi_sim:中文
        :return:
        """
        # 为防止截图包含高亮影响识别，元素不进行高亮
        captcha_webElement=self._change_element_to_webElement_type(element,highlight_seconds)
        left = captcha_webElement.location['x']
        top = captcha_webElement.location['y']
        right = captcha_webElement.location['x'] + captcha_webElement.size['width']
        bottom = captcha_webElement.location['y'] + captcha_webElement.size['height']
        # 首先进行屏幕截图
        captcha_image_file_name=DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_')+'captcha.png'
        captcha_image_file_name=os.path.abspath('output/' + self._config.current_browser + '/' + captcha_image_file_name)
        self._driver.get_screenshot_as_file(captcha_image_file_name)
        img=Image.open(captcha_image_file_name)
        # 验证码图片裁切并保存
        img=img.crop((left,top,right,bottom))
        img.save(captcha_image_file_name)
        # 识别图片验证码
        captcha=CaptchaRecognitionTool.captchaRecognition(captcha_image_file_name,language)
        captcha=captcha.strip()
        captcha=captcha.replace(' ','')
        return captcha

    def get_table_data(self,element,data_type='text'):
        """
        以二维数组返回表格每一行的每一列的数据[[row1][row2][colume1,clume2]]
        :param element:
        :param data_type: text-返回表格文本内容,html-返回表格html内容,webElement-返回表格元素
        :return:
        """
        if isinstance(element, ElementInfo):
            # 由于表格定位经常会出现【StaleElementReferenceException: Message: stale element reference: element is not attached to the page document 】异常错误,
            # 解决此异常只需要用显示等待，保证元素存在即可，显示等待类型中visibility_of_all_elements_located有实现StaleElementReferenceException异常捕获,
            # 所以强制设置表格定位元素时使用VISIBILITY_OF
            element.wait_type=Wait_By.VISIBILITY_OF
            webElement = self.getElement(element)
        elif isinstance(element,WebElement):
            webElement = element
        else:
            return None
        table_data = []
        table_trs = webElement.find_elements_by_tag_name('tr')
        try:
            # 为防止表格内的内容变化导致无法获取内容,进行异常捕获
            for tr in table_trs:
                tr_data=[]
                tr_tds = tr.find_elements_by_tag_name('td')
                if data_type.lower()=='text':
                    for td in tr_tds:
                        tr_data.append(td.text)
                elif data_type.lower()=='html':
                    for td in tr_tds:
                        tr_data.append(td.get_attribute('innerHTML'))
                elif data_type.lower()=='webelement':
                    tr_data=tr_tds
                table_data.append(tr_data)
        except StaleElementReferenceException as e:
            print('获取表格内容异常:'+e.msg)
        return table_data

    def getElement(self,elementInfo,highlight_seconds=5):
        """
        定位单个元素
        :param highlight_seconds:
        :param elementInfo:
        :return:
        """
        webElement=None
        locator_type=elementInfo.locator_type
        locator_value=elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds
        wait_expected_value = elementInfo.wait_expected_value
        if wait_expected_value:
            wait_expected_value = wait_expected_value

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.TITLE_IS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.title_is(wait_expected_value))
        elif wait_type == Wait_By.TITLE_CONTAINS:
            webElement = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.title_contains(wait_expected_value))
        elif wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.presence_of_element_located((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_TO_BE_CLICKABLE:
            webElement = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.element_to_be_clickable((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_LOCATED_TO_BE_SELECTED:
            webElement = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.element_located_to_be_selected((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver,wait_seconds).until((expected_conditions.visibility_of_all_elements_located((locator_type,locator_value))))
            if len(webElements)>0:
                webElement=webElements[0]
        else:
            if locator_type==By.ID:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_id(locator_value))
            elif locator_type==By.NAME:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_name(locator_value))
            elif locator_type==By.LINK_TEXT:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_link_text(locator_value))
            elif locator_type==By.XPATH:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_xpath(locator_value))
            elif locator_type==By.PARTIAL_LINK_TEXT:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_partial_link_text(locator_value))
            elif locator_type==By.CSS_SELECTOR:
                webElement=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_css_selector(locator_value))
            elif locator_type==By.CLASS_NAME:
                webElement = WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_class_name(locator_value))
            elif locator_type==By.TAG_NAME:
                webElement = WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_element_by_tag_name(locator_value))
        if not wait_type==Wait_By.TITLE_IS and not wait_type==Wait_By.TITLE_CONTAINS:
            self.highLight(webElement,highlight_seconds)
        return webElement

    def getElements(self,elementInfo,highlight_seconds=5):
        """
        定位多个元素
        :param highlight_seconds:
        :param elementInfo:
        :return:
        """
        webElements=None
        locator_type=elementInfo.locator_type
        locator_value=elementInfo.locator_value
        wait_type = elementInfo.wait_type
        wait_seconds = elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            webElements = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.presence_of_all_elements_located((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF:
            webElements = WebDriverWait(self._driver, wait_seconds).until(expected_conditions.visibility_of_all_elements_located((locator_type,locator_value)))
        else:
            if locator_type==By.ID:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_id(locator_value))
            elif locator_type==By.NAME:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_name(locator_value))
            elif locator_type==By.LINK_TEXT:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_link_text(locator_value))
            elif locator_type==By.XPATH:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_xpath(locator_value))
            elif locator_type==By.PARTIAL_LINK_TEXT:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_partial_link_text(locator_value))
            elif locator_type==By.CSS_SELECTOR:
                webElements=WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_css_selector(locator_value))
            elif locator_type==By.CLASS_NAME:
                webElements = WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_class_name(locator_value))
            elif locator_type==By.TAG_NAME:
                webElements = WebDriverWait(self._driver,wait_seconds).until(lambda driver:driver.find_elements_by_tag_name(locator_value))
        for webElement in webElements:
            self.highLight(webElement,highlight_seconds)
        return webElements

    def getSubElement(self,parent_element,sub_elementInfo,highlight_seconds=5):
        """
        获得元素的单个子元素
        :param highlight_seconds:
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        if isinstance(parent_element,ElementInfo):
            webElement=self.getElement(parent_element)
        elif isinstance(parent_element,WebElement):
            webElement=parent_element
        else:
            return None
        if not isinstance(sub_elementInfo,ElementInfo):
            return None

        # 通过父元素查找子元素
        locator_type=sub_elementInfo.locator_type
        locator_value=sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElement =WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_id(locator_value))
        elif locator_type == By.NAME:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_name(locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_link_text(locator_value))
        elif locator_type == By.XPATH:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_xpath(locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_partial_link_text(locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_css_selector(locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_class_name(locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElement = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_element_by_tag_name(locator_value))
        else:
            return None
        self.highLight(subWebElement,highlight_seconds)
        return subWebElement

    def getSubElements(self, parent_element, sub_elementInfo,highlight_seconds=5):
        """
        获得元素的多个子元素
        :param highlight_seconds:
        :param parent_element: 父元素
        :param sub_elementInfo: 子元素,只能提供pojo.elementInfo.ElementInfo类型
        :return:
        """
        if isinstance(parent_element,ElementInfo):
            webElement=self.getElement(parent_element)
        elif isinstance(parent_element,WebElement):
            webElement=parent_element
        else:
            return None
        if not isinstance(sub_elementInfo,ElementInfo):
            return None

        # 通过父元素查找多个子元素
        locator_type = sub_elementInfo.locator_type
        locator_value = sub_elementInfo.locator_value
        wait_seconds = sub_elementInfo.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        if locator_type == By.ID:
            subWebElements =WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_id(locator_value))
        elif locator_type == By.NAME:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_name(locator_value))
        elif locator_type == By.LINK_TEXT:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_link_text(locator_value))
        elif locator_type == By.XPATH:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_xpath(locator_value))
        elif locator_type == By.PARTIAL_LINK_TEXT:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_partial_link_text(locator_value))
        elif locator_type == By.CSS_SELECTOR:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_css_selector(locator_value))
        elif locator_type == By.CLASS_NAME:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_class_name(locator_value))
        elif locator_type == By.TAG_NAME:
            subWebElements = WebDriverWait(webElement,wait_seconds).until(lambda webElement:webElement.find_elements_by_tag_name(locator_value))
        else:
            return None
        for subWebElement in subWebElements:
            self.highLight(subWebElement,highlight_seconds)
        return subWebElements

    def explicit_wait_page_title(self,elementInfo):
        """
        显式等待页面title
        :param elementInfo:
        :return:
        """
        self.getElement(elementInfo)

    def highLight(self,webElement,seconds=5):
        try:
            # 进行StaleElementReferenceException异常捕获
            self._driver.execute_script("element = arguments[0];" +
                                  "original_style = element.getAttribute('style');" +
                                  "element.setAttribute('style', original_style + \";" +
                                  " border: 3px dashed rgb(250,0,255);\");" +
                                  "setTimeout(function(){element.setAttribute('style', original_style);}, "+str(seconds*1000)+");",
                                        webElement)
        except StaleElementReferenceException as e:
            print('高亮StaleElementReferenceException异常:'+e.msg)

    def getDriver(self):
        return self._driver

    def close(self):
        self._driver.__exit__()
