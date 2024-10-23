#
# browser_operator.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.673Z+08:00
# @last-modified 2024-10-23T16:17:50.393Z+08:00
#

from common.date_time_tool import DateTimeTool
from page_objects.wait_type import WaitType as Wait_By
from page_objects.element_info import ElementInfo
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from skimage.io import imread
from skimage.io import imsave
from typing import Any
from typing import List
from typing import Union
import allure
import os

# JSON Wire protocol：https://www.selenium.dev/documentation/legacy/json_wire_protocol/
# API：https://www.selenium.dev/selenium/docs/api/py/api.html
# chrome浏览器相关命令行操作：https://peter.sh/experiments/chromium-command-line-switches/

class Browser_Operator:
    
    def __init__(self,driver:WebDriver):
        self.driver=driver

    def _change_element_to_web_element_type(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->WebElement:
        if isinstance(element, ElementInfo):
            element=self.get_element(element,highlight_seconds)
        return element
    
    def add_cookie(self,cookie:dict)->None:
        """ 
            driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/'}) 
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})
            driver.add_cookie({'name': 'foo', 'value': 'bar', 'sameSite': 'Strict'})
        Args:
            cookie (dict): _description_
        """
        self.driver.add_cookie(cookie)
    
    def delete_cookie(self,name:str)->None:
        self.driver.delete_cookie(name)
    
    def delete_all_cookies(self)->None:
        self.driver.delete_all_cookies()
        
    def get_cookie(self,name:str)->dict:
        return self.driver.get_cookie(name)
    
    def get_cookies(self)->List[dict]:
        return self.driver.get_cookies()

    def get(self,url:str)->str:
        self.driver.get(url)

    def get_current_url(self)->str:
        return self.driver.current_url

    def get_title(self)->str:
        return self.driver.title

    def get_text(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->str:
        web_element=self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            return web_element.text
    
    def get_element_rect(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->dict:
        web_element=self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            return web_element.rect

    def click(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->None:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element.click()

    def submit(self,element:Union[ElementInfo,WebElement],highlight_seconds=5)->None:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element.submit()

    def send_text(self,element:Union[ElementInfo,WebElement],text:str,highlight_seconds:float=5)->None:
        text=text
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element.clear()
            web_element.send_keys(text)

    def send_keys(self,element:Union[ElementInfo,WebElement],keys:str,highlight_seconds:float=5)->None:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element.send_keys(keys)

    def is_displayed(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->bool:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            flag=web_element.is_displayed()
            return flag

    def is_enabled(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->bool:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            flag = web_element.is_enabled()
            return flag

    def is_selected(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5)->bool:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            flag = web_element.is_selected()
            return flag

    def select_dropDownBox_by_value(self,element:Union[ElementInfo,WebElement],value:str,highlight_seconds:float=5)->None:
        """适用单选下拉框

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            value (str): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.select_by_value(value)            

    def select_dropDownBox_by_text(self,element:Union[ElementInfo,WebElement],text:str,highlight_seconds:float=5)->None:
        """适用单选下拉框

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            text (str): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.select_by_visible_text(text)

    def select_dropDownBox_by_index(self,element:Union[ElementInfo,WebElement],index,highlight_seconds:float=5)->None:
        """适用单选下拉框,下标从0开始

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            index (_type_): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.select_by_index(index)

    def select_dropDownBox_by_values(self,element:Union[ElementInfo,WebElement],values:list,highlight_seconds:float=5)->None:
        """适用多选下拉框

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            values (list): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.deselect_all()
            for value in values:
                web_element.select_by_value(value)

    def select_dropDownBox_by_texts(self,element:Union[ElementInfo,WebElement],texts:list,highlight_seconds:float=5)->None:
        """适用多选下拉框

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            texts (list): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.deselect_all()
            for text in texts:
                web_element.select_by_visible_text(text)

    def select_dropDownBox_by_indexs(self,element:Union[ElementInfo,WebElement],indexs:list,highlight_seconds:float=5)->None:
        """适用多选下拉框，下标从0开始

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            indexs (list): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element=Select(web_element)
            web_element.deselect_all()
            for index in indexs:
                web_element.select_by_index(index)

    def get_window_handles(self)->List[str]:
        """获得窗口句柄

        Returns:
            List[str]: _description_
        """
        return self.driver.window_handles

    def get_current_window_handle(self)->str:
        """获得当前的窗口句柄

        Returns:
            str: _description_
        """
        return  self.driver.current_window_handle

    def switch_to_window(self,window_name:str)->None:
        self.driver.switch_to.window(window_name)

    def maximize_window(self)->None:
        self.driver.maximize_window()

    def switch_to_frame(self,frame_reference)->None:
        """_summary_

        Args:
            frame_reference (_type_): 支持窗口名、frame索引、(i)frame元素
        """
        frame_reference=self._change_element_to_web_element_type(frame_reference)
        self.driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self)->None:
        self.driver.switch_to.parent_frame()

    def page_forward(self)->None:
        self.driver.forward()

    def page_back(self)->None:
        self.driver.back()

    def web_alert(self, action_type:str='accept')->None:
        """        

        Args:
            action_type (str, optional): accept、dismiss. Defaults to 'accept'.
        """
        if action_type:
            action_type.lower()
        alert = self.driver.switch_to.alert
        if action_type == 'accept':
            alert.accept()
        elif action_type == 'dismiss':
            alert.dismiss()

    def get_alert_text(self)->str:
        alert=self.driver.switch_to.alert
        return alert.text
    
    def send_alert_text(self,text:str)->None:
        alert=self.driver.switch_to.alert
        alert.send_keys(text)

    def get_screenshot(self,fileName:str)->None:
        fileName=DateTimeTool.get_now_time('%Y%m%d%H%M%S%f_')+fileName
        allure.attach(name=fileName,body=self.driver.get_screenshot_as_png(),attachment_type=allure.attachment_type.PNG)

    def refresh(self)->None:
        self.driver.refresh()

    def upload_file(self,element:Union[ElementInfo,WebElement],filePath:str,highlight_seconds:float=5)->None:
        """适用于元素为input且type="file"的文件上传

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            filePath (str): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            web_element.send_keys(os.path.abspath(filePath))

    def get_property(self,element:Union[ElementInfo,WebElement],property_name:str,highlight_seconds:float=5) -> Union[str,bool,WebElement,dict]:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            return web_element.get_property(property_name)

    def get_attribute(self,element:Union[ElementInfo,WebElement],attribute_name:str,highlight_seconds:float=5)->Any:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            return web_element.get_attribute(attribute_name)

    def get_element_outer_html(self,element:Union[ElementInfo,WebElement])->str:
        return self.get_attribute(element,'outerHTML')

    def get_element_inner_html(self, element:Union[ElementInfo,WebElement])->str:
        return self.get_attribute(element,'innerHTML')

    def get_page_source(self)->str:
        """由于Android和IOS没有标准的XML层级，appium在获取XML时是创建一个XML文档，所以该方法较为耗时

        Returns:
            str: _description_
        """
        return self.driver.page_source

    def get_element_rgb(self,element:Union[ElementInfo,WebElement],x_percent:float=0,y_percent:float=0)->list:
        """获得元素上的像素的rgb值,默认返回元素左上角坐标轴

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            x_percent (float, optional): x轴百分比位置,范围0~1 Defaults to 0.
            y_percent (float, optional): y轴百分比位置,范围0~1. Defaults to 0.

        Returns:
            _type_: _description_
        """
        ndarray=imread(self.save_element_image(element,'element_rgb'))
        height,width,channel=ndarray.shape
        pix_x=int(width*x_percent)
        pix_y=int(height*y_percent)
        if not pix_x==0:
            pix_x=pix_x-1
        if not pix_y==1:
            pix_y=pix_y-1
        return list(ndarray[pix_y,pix_x])

    def save_element_image(self, element:Union[ElementInfo,WebElement], image_file_name:str, highlight_seconds:float=0)->str:
        web_element = self._change_element_to_web_element_type(element, highlight_seconds)
        left = web_element.location['x']
        top = web_element.location['y']
        right = web_element.location['x'] + web_element.size['width']
        bottom = web_element.location['y'] + web_element.size['height']
        # 进行屏幕截图
        image_file_name = DateTimeTool.get_now_time('%Y%m%d%H%M%S%f_') + '%s.png'%image_file_name
        if not os.path.exists('output/tmp/web_ui/'+self.driver.name):
            os.mkdir('output/tmp/web_ui/'+self.driver.name)
        image_file_name = os.path.abspath(
            'output/tmp/web_ui/' + self.driver.name + '/' + image_file_name)
        self.driver.get_screenshot_as_file(image_file_name)
        ndarray=imread(image_file_name)
        # 图片裁切并保存
        new_ndarray=ndarray[top:bottom,left:right]
        imsave(image_file_name,new_ndarray)
        return image_file_name

    def get_captcha(self, element:Union[ElementInfo,WebElement], language='eng')->str:
        """识别图片验证码，如需使用该方法必须配置jpype1、字体库等依赖环境

        Args:
            element (_type_): 验证码图片元素
            language (str, optional): eng:英文,chi_sim:中文. Defaults to 'eng'.

        Returns:
            str: _description_
        """
        # 为防止截图包含高亮影响识别，元素不进行高亮
        # 识别图片验证码
        from common.captchaRecognitionTool import CaptchaRecognitionTool
        captcha_image_file_name = self.save_element_image(element, 'captcha')
        captcha = CaptchaRecognitionTool.captchaRecognition(captcha_image_file_name, language)
        captcha = captcha.strip()
        captcha = captcha.replace(' ', '')
        return captcha

    def get_table_data(self,element:Union[ElementInfo,WebElement],data_type:str='text')->List[list]:
        """以二维数组返回表格每一行的每一列的数据[[row1][row2][colume1,clume2]]

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            data_type (str, optional): text-返回表格文本内容,html-返回表格html内容,web_element-返回表格元素. Defaults to 'text'.

        Returns:
            _type_: _description_
        """        
        if isinstance(element, ElementInfo):
            # 由于表格定位经常会出现【StaleElementReferenceException: Message: stale element reference: element is not attached to the page document 】异常错误,
            # 解决此异常只需要用显示等待，保证元素存在即可，显示等待类型中visibility_of_all_elements_located有实现StaleElementReferenceException异常捕获,
            # 所以强制设置表格定位元素时使用VISIBILITY_OF
            element.wait_type=Wait_By.VISIBILITY_OF
            web_element = self.get_element(element)
        elif isinstance(element,WebElement):
            web_element = element
        else:
            return None
        table_data = []
        table_trs = web_element.find_elements(By.TAG_NAME,'tr')
        try:
            # 为防止表格内的内容变化导致无法获取内容,进行异常捕获
            for tr in table_trs:
                tr_data=[]
                tr_tds = tr.find_elements(By.TAG_NAME,'td')
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

    def scroll_to_show(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=5,is_top_align:bool=True)->None:
        """滚动页面直至元素可见

        Args:
            element (Union[ElementInfo,WebElement]): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.
            is_top_align (bool, optional):  是否元素与窗口顶部对齐，否则与窗口底部对齐. Defaults to True.
        """
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        if web_element:
            if is_top_align:
                self.driver.execute_script("arguments[0].scrollIntoView();", web_element)
            else:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", web_element)
    
    def move_by_offset(self,x:float,y:float)->None:
        """移动鼠标到指定坐标，x为横坐标，y为纵坐标

        Args:
            x (float): _description_
            y (float): _description_
        """
        return ActionChains(self.driver).move_by_offset(x,y).perform()
        
    def move_to_element(self,element:Union[ElementInfo,WebElement],highlight_seconds:float=0)->None:
        web_element = self._change_element_to_web_element_type(element,highlight_seconds)
        ActionChains(self.driver).move_to_element(web_element).perform()

    def get_element(self,element:ElementInfo,highlight_seconds:float=5)->WebElement:
        """定位单个元素

        Args:
            element (ElementInfo): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.

        Returns:
            WebElement: _description_
        """
        web_element=None
        locator_type=element.locator_type
        locator_value=element.locator_value
        wait_type = element.wait_type
        wait_seconds = element.wait_seconds
        wait_expected_value = element.wait_expected_value
        relative_element = element.relative_element
        relative_type = element.relative_type

        # 查找元素,为了保证元素被定位,都进行显式等待,部分返回并非是WebElement对象
        # 相对位置定位方式
        if relative_element and relative_type:
            tmp_element=element
            tmp_element.relative_element=None
            tmp_element.relative_type=None
            tmp_web_element=self.get_element(tmp_element)
            if relative_type == 'above':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).above(tmp_web_element)
            elif relative_type == 'below':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).below(tmp_web_element)
            elif relative_type == 'to_left_of':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_left_of(tmp_web_element)
            elif relative_type == 'to_right_of':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_right_of(tmp_web_element)
            elif relative_type == 'near':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).near(tmp_web_element)
            else:
                relative_locattor={}
            web_element=self.driver.find_element(relative_locattor)
            if isinstance(web_element,WebElement):
                self.highLight(web_element,highlight_seconds)
            return web_element
        # 状态定位方式
        if wait_type == Wait_By.ALERT_IS_PRESENT:
            web_element = WebDriverWait(self.driver,wait_seconds).until(expected_conditions.alert_is_present())
        elif wait_type == Wait_By.ELEMENT_ATTRIBUTE_TO_INCLUDE:
            web_element = WebDriverWait(self.driver,wait_seconds).until(expected_conditions.element_attribute_to_include((locator_type, locator_value),wait_expected_value))
        elif wait_type == Wait_By.ELEMENT_TO_BE_CLICKABLE:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.element_to_be_clickable((locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_TO_BE_SELECTED:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.element_to_be_selected(self.driver.find_element(locator_type, locator_value)))
        elif wait_type == Wait_By.ELEMENT_LOCATED_TO_BE_SELECTED:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.element_located_to_be_selected((locator_type, locator_value)))
        elif wait_type == Wait_By.FRAME_TO_BE_AVAILABLE_AND_SWITCH_TO_IT:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.frame_to_be_available_and_switch_to_it((locator_type, locator_value)))
        elif wait_type == Wait_By.FRESHNESS_OF:
            web_element = WebDriverWait(self.driver, wait_seconds).until(not expected_conditions.staleness_of(self.driver.find_element(locator_type, locator_value)))
        elif wait_type == Wait_By.INVISIBILITY_OF_ELEMENT_LOCATED:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.invisibility_of_element_located((locator_type, locator_value)))
        elif wait_type == Wait_By.NUMBER_OF_WINDOWS_TO_BE:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.number_of_windows_to_be(wait_expected_value))
        elif wait_type == Wait_By.PRESENCE_OF_ELEMENT_LOCATED:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.presence_of_element_located((locator_type, locator_value)))
        elif wait_type == Wait_By.STALENESS_OF:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.staleness_of(self.driver.find_element(locator_type, locator_value)))
        elif wait_type == Wait_By.TEXT_TO_BE_PRESENT_IN_ELEMENT:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.text_to_be_present_in_element((locator_type, locator_value)))
        elif wait_type == Wait_By.TITLE_IS:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.title_is(wait_expected_value))
        elif wait_type == Wait_By.TITLE_CONTAINS:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.title_contains(wait_expected_value))
        elif wait_type == Wait_By.URL_TO_BE:
            web_element = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.url_to_be(wait_expected_value))
        elif wait_type == Wait_By.VISIBILITY_OF:
            web_element = WebDriverWait(self.driver,wait_seconds).until(expected_conditions.visibility_of(self.driver.find_element(locator_type,locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF_ELEMENT_LOCATED:
            web_element = WebDriverWait(self.driver,wait_seconds).until(expected_conditions.visibility_of_element_located((locator_type,locator_value)))
        else:
        # 常规定位方式
            web_element=WebDriverWait(self.driver,wait_seconds).until(lambda driver:driver.find_element(locator_type,locator_value))
        if isinstance(web_element,WebElement):
            self.highLight(web_element,highlight_seconds)
        return web_element

    def get_elements(self,element:ElementInfo,highlight_seconds:float=5)->List[WebElement]:
        """定位多个元素

        Args:
            element (ElementInfo): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.

        Returns:
            List[WebElement]: _description_
        """
        web_elements=None
        locator_type=element.locator_type
        locator_value=element.locator_value
        wait_type = element.wait_type
        wait_seconds = element.wait_seconds
        relative_element = element.relative_element
        relative_type = element.relative_type

        # 查找元素,为了保证元素被定位,都进行显式等待,部分返回并非是WebElement对象
        # 相对位置定位方式
        if relative_element and relative_type:
            tmp_element=element
            tmp_element.relative_element=None
            tmp_element.relative_type=None
            tmp_web_element=self.get_element(tmp_element)
            if relative_type == 'above':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).above(tmp_web_element)
            elif relative_type == 'below':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).below(tmp_web_element)
            elif relative_type == 'to_left_of':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_left_of(tmp_web_element)
            elif relative_type == 'to_right_of':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_right_of(tmp_web_element)
            elif relative_type == 'near':
                relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).near(tmp_web_element)
            else:
                relative_locattor={}
            web_elements=self.driver.find_elements(relative_locattor)
            for web_element in web_elements:
                if isinstance(web_element,WebElement):
                    self.highLight(web_element,highlight_seconds)
            return web_elements
        # 状态定位方式
        if wait_type == Wait_By.PRESENCE_OF_ALL_ELEMENTS_LOCATED:
            web_elements = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.presence_of_all_elements_located((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF_ALL_ELEMENTS_LOCATED:
            web_elements = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.visibility_of_all_elements_located((locator_type,locator_value)))
        else:
        # 常规定位方式
            web_elements=WebDriverWait(self.driver,wait_seconds).until(lambda driver:driver.find_elements(locator_type,locator_value))
        for web_element in web_elements:
            if isinstance(web_element,WebElement):
                self.highLight(web_element,highlight_seconds)
        return web_elements

    def get_sub_element(self,parent_element:Union[ElementInfo,WebElement],sub_element:ElementInfo,highlight_seconds:float=5)->WebElement:
        """获得元素的单个子元素

        Args:
            parent_element (Union[ElementInfo,WebElement]): _description_
            sub_element (ElementInfo): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.

        Returns:
            WebElement: _description_
        """
        web_element=self._change_element_to_web_element_type(parent_element)
        if not web_element:
            return None
        if not isinstance(sub_element,ElementInfo):
            return None

        # 通过父元素查找子元素
        locator_type=sub_element.locator_type
        locator_value=sub_element.locator_value
        wait_seconds = sub_element.wait_seconds
        # 查找元素,为了保证元素被定位,都进行显式等待
        sub_web_element = WebDriverWait(web_element,wait_seconds).until(lambda web_element:web_element.find_element(locator_type,locator_value))
        if isinstance(sub_web_element,WebElement):
            self.highLight(sub_web_element,highlight_seconds)
        return sub_web_element

    def get_sub_elements(self, parent_element:Union[ElementInfo,WebElement], sub_element:ElementInfo,highlight_seconds:float=5)->List[WebElement]:
        """获得元素的多个子元素

        Args:
            parent_element (Union[ElementInfo,WebElement]): _description_
            sub_element (ElementInfo): _description_
            highlight_seconds (float, optional): _description_. Defaults to 5.

        Returns:
            List[WebElement]: _description_
        """
        web_element=self._change_element_to_web_element_type(parent_element)
        if not web_element:
            return None
        if not isinstance(sub_element,ElementInfo):
            return None

        # 通过父元素查找多个子元素
        locator_type = sub_element.locator_type
        locator_value = sub_element.locator_value
        wait_seconds = sub_element.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        sub_web_elements =WebDriverWait(web_element,wait_seconds).until(lambda web_element:web_element.find_elements(locator_type,locator_value))
        for sub_web_element in sub_web_elements:
            if isinstance(sub_web_element,WebElement):
                self.highLight(sub_web_element,highlight_seconds)
        return sub_web_elements

    def explicit_wait_page_title(self,element:ElementInfo)->None:
        """显式等待页面title

        Args:
            element (ElementInfo): _description_
        """
        self.get_element(element)

    def highLight(self,web_element:WebElement,seconds:float=5)->None:
        try:
            # 进行StaleElementReferenceException异常捕获
            self.driver.execute_script("element = arguments[0];" +
                                  "original_style = element.getAttribute('style');" +
                                  "element.setAttribute('style', original_style + \";" +
                                  " border: 3px dashed rgb(250,0,0);\");" +
                                  "setTimeout(function(){element.setAttribute('style', original_style);}, "+str(seconds*1000)+");",
                                        web_element)
        except StaleElementReferenceException as e:
            print('高亮StaleElementReferenceException异常:'+e.msg)

    def close(self)->None:
        self.driver.close()
    
    def quit(self)->None:
        self.driver.quit()