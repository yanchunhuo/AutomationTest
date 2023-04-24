#
# app_operator.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.201Z+08:00
# @last-modified 2023-04-24T16:32:15.704Z+08:00
#

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from common.dateTimeTool import DateTimeTool
from common.httpclient.doRequest import DoRequest
from page_objects.create_element import Create_Element
from page_objects.wait_type import Wait_Type as Wait_By
from page_objects.element_info import Element_Info
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.action_chains import ActionChains
from skimage.io import imread
from skimage.io import imsave
from typing import List,Dict
from typing import Union

import allure
import base64
import ujson
import os

class AppOperator:

    def __init__(self,driver:WebDriver,appium_hub:str):
        self.doRequest=DoRequest(appium_hub)
        self.doRequest.setHeaders({'Content-Type':'application/json'})
        self.driver=driver
        self.session_id=driver.session_id
        # 获得设备支持的性能数据类型
        self.performance_types=ujson.loads(self.doRequest.post_with_form('/session/'+self.session_id+'/appium/performanceData/types').body)['value']
        # 获取当前窗口大小
        self.window_size=self.get_window_size()
        # 获得当前窗口的位置
        self.window_rect=self.get_window_rect()

    def _change_element_to_web_element_type(self,element:Union[Element_Info,WebElement])->WebElement:
        if isinstance(element, Element_Info):
            web_element=self.get_element(element)
        elif isinstance(element,WebElement):
            web_element=element
        else:
            return element
        return web_element

    def get(self,url:str)->None:
        self.driver.get(url)

    def get_current_url(self)->str:
        return self.driver.current_url

    def get_title(self)->str:
        return self.driver.title

    def get_text(self,element:Union[Element_Info,WebElement])->str:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.text
        
    def get_tag_name(self,element:Union[Element_Info,WebElement])->str:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.tag_name

    def click(self,element:Union[Element_Info,WebElement])->None:
        """点击元素中心点
            1、如果元素被遮挡，则返回点击中断错误
            2、如果元素在视图窗口外，则返回元素不可交互错误
            注：并非所有驱动程序都会自动将元素滚动到视图中，并且可能需要滚动到以与其交互

        Args:
            element (Union[Element_Info,WebElement]): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element.click()
        
    def click_web_element(self,element:Union[Element_Info,WebElement])->None:
        """由于混合应用存在点击无效的情况，故混合应用的点击采用selenium的tab操作确保能够正常点击

        Args:
            element (Union[Element_Info,WebElement]): _description_
        """
        
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            actions=ActionChains(self.driver)
            actions.click(web_element)
            actions.tap(web_element).perform()

    def submit(self,element:Union[Element_Info,WebElement])->None:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element.submit()

    def send_text(self,element:Union[Element_Info,WebElement],text:str)->None:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element.clear()
            web_element.send_keys(text)
    
    def clear_text(self,element:Union[Element_Info,WebElement])->None:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element.clear()

    def is_displayed(self,element:Union[Element_Info,WebElement])->bool:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.is_displayed()

    def is_enabled(self,element:Union[Element_Info,WebElement])->bool:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.is_enabled()

    def is_selected(self,element:Union[Element_Info,WebElement])->bool:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.is_selected()

    def select_dropDownBox_by_value(self,element:Union[Element_Info,WebElement],value:str)->None:
        """适用单选下拉框

        Args:
            element (Union[Element_Info,WebElement]): _description_
            value (str): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.select_by_value(value)

    def select_dropDownBox_by_text(self,element:Union[Element_Info,WebElement],text:str)->None:
        """适用单选下拉框

        Args:
            element (Union[Element_Info,WebElement]): _description_
            text (str): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.select_by_visible_text(text)

    def select_dropDownBox_by_index(self,element:Union[Element_Info,WebElement],index:int)->None:
        """适用单选下拉框,下标从0开始

        Args:
            element (_type_): _description_
            index (_type_): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.select_by_index(index)

    def select_dropDownBox_by_values(self,element:Union[Element_Info,WebElement],values:List[str])->None:
        """适用多选下拉框

        Args:
            element (Union[Element_Info,WebElement]): _description_
            values (List[str]): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.deselect_all()
            for value in values:
                web_element.select_by_value(value)

    def select_dropDownBox_by_texts(self,element:Union[Element_Info,WebElement],texts:List[str])->None:
        """适用多选下拉框

        Args:
            element (Union[Element_Info,WebElement]): _description_
            texts (List[str]): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.deselect_all()
            for text in texts:
                web_element.select_by_visible_text(text)

    def select_dropDownBox_by_indexs(self,element:Union[Element_Info,WebElement],indexs:List[int])->None:
        """适用多选下拉框，下标从0开始

        Args:
            element (Union[Element_Info,WebElement]): _description_
            indexs (List[int]): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element = Select(web_element)
            web_element.deselect_all()
            for index in indexs:
                web_element.select_by_index(index)

    def get_window_handles(self)->List[str]:
        """获得窗口句柄，仅适用于web

        Returns:
            _type_: _description_
        """
        return self.driver.window_handles

    def switch_to_window(self,window_name:str)->None:
        """仅适用于web

        Args:
            window_name (str): _description_
        """
        self.driver.switch_to.window(window_name)

    def switch_to_frame(self,frame_reference)->None:
        """仅适用于web

        Args:
            frame_reference (_type_): 支持窗口名、frame索引、(i)frame元素
        """
        frame_reference=self._change_element_to_web_element_type(frame_reference)
        self.driver.switch_to.frame(frame_reference)

    def page_forward(self)->None:
        """仅适用于web
        """
        self.driver.forward()

    def page_back(self)->None:
        """仅适用于web
        """
        self.driver.back()

    def web_alert(self,action_type:str='accept')->None:
        """仅适用于web

        Args:
            action_type (str, optional): accept、dismiss. Defaults to 'accept'.
        """
        if action_type:
            action_type.lower()
        alert = self.driver.switch_to.alert
        if action_type=='accept':
            alert.accept()
        elif action_type=='dismiss':
            alert.dismiss()

    def get_alert_text(self)->str:
        """仅适用于web

        Returns:
            str: _description_
        """
        alert=self.driver.switch_to.alert
        return alert.text
    
    def scroll_to_show(self,element:Union[Element_Info,WebElement],is_top_align:bool=True)->None:
        """仅适用于web,滚动页面直至元素可见
        https://appium.io/docs/en/commands/web/execute/index.html
        
        Args:
            element (Union[Element_Info,WebElement]): _description_
            is_top_align (bool, optional): 是否元素与窗口顶部对齐，否则与窗口底部对齐. Defaults to True.
        """
        web_element = self._change_element_to_web_element_type(element)
        if web_element:
            if is_top_align:
                self.driver.execute_script("arguments[0].scrollIntoView();", web_element)
            else:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", web_element)

    def get_screenshot(self,fileName:str)->None:
        fileName=DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_')+fileName
        allure.attach(name=fileName,body=self.driver.get_screenshot_as_png(),attachment_type=allure.attachment_type.PNG)

    def refresh(self)->None:
        self.driver.refresh()

    def upload_file(self,element:Union[Element_Info,WebElement],filePath)->None:
        """仅适用于web，适用于元素为input且type="file"的文件上传

        Args:
            element (Union[Element_Info,WebElement]): _description_
            filePath (_type_): _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            web_element.send_keys(os.path.abspath(filePath))

    def switch_to_parent_frame(self)->None:
        """切换到父frame(仅适用于web)
        """
        self.driver.switch_to.parent_frame()

    def get_property(self,element:Union[Element_Info,WebElement],property_name:str)->str:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.get_property(property_name)

    def get_attribute(self,element:Union[Element_Info,WebElement],attribute_name:str)->str:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.get_attribute(attribute_name)

    def get_element_outer_html(self,element:Union[Element_Info,WebElement])->str:
        return self.get_attribute(element,'outerHTML')

    def get_element_inner_html(self, element:Union[Element_Info,WebElement])->str:
        return self.get_attribute(element,'innerHTML')

    def get_page_source(self)->str:
        """获得app的层次结构xml，web页面源码

        Returns:
            str: _description_
        """
        return self.driver.page_source

    def get_element_rgb(self,element:Union[Element_Info,WebElement],x_percent:float=0,y_percent:float=0)->list:
        """获得元素上的rgb值,默认返回元素左上角坐标轴

        Args:
            element (Union[Element_Info,WebElement]): _description_
            x_percent (float, optional): x轴百分比位置,范围0~1. Defaults to 0.
            y_percent (float, optional): y轴百分比位置,范围0~1. Defaults to 0.

        Returns:
            list: _description_
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

    def save_element_image(self, element:Union[Element_Info,WebElement], image_file_name:str)->str:
        """_summary_

        Args:
            element (Union[Element_Info,WebElement]): _description_
            image_file_name (str): _description_

        Returns:
            str: _description_
        """
        web_element = self._change_element_to_web_element_type(element)
        left = web_element.location['x']
        top = web_element.location['y']
        right = web_element.location['x'] + web_element.size['width']
        bottom = web_element.location['y'] + web_element.size['height']
        window_left=self.window_rect['x']
        window_top=self.window_rect['y']
        window_right=left+self.window_rect['width']
        window_bottom=top+self.window_rect['height']
        # 进行屏幕截图
        image_file_name = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + '%s.png'%image_file_name
        if not os.path.exists('output/tmp/app_ui/'):
            os.mkdir('output/tmp/app_ui/')
        image_file_name = os.path.abspath('output/tmp/app_ui/' + image_file_name)
        self.driver.get_screenshot_as_file(image_file_name)
        ndarray=imread(image_file_name)
        # 裁切应用区域图片并保存
        new_ndarray=ndarray[window_top:window_bottom,window_left:window_right]
        imsave(image_file_name,new_ndarray)
        # 裁切元素区域图片并保存
        ndarray=imread(image_file_name)
        new_ndarray=ndarray[top:bottom,left:right]
        imsave(image_file_name,new_ndarray)
        return image_file_name

    def get_captcha(self,element:Union[Element_Info,WebElement],language:str='eng')->str:
        """识别图片验证码，如需使用该方法必须配置jpype1、字体库等依赖环境
    
        Args:
            element (Union[Element_Info,WebElement]): 验证码图片元素
            language (str, optional): eng:英文,chi_sim:中文. Defaults to 'eng'.

        Returns:
            str: _description_
        """
        # 识别图片验证码
        from common.captchaRecognitionTool import CaptchaRecognitionTool
        captcha_image_file_name=self.save_element_image(element,'captcha')
        captcha=CaptchaRecognitionTool.captchaRecognition(captcha_image_file_name,language)
        captcha=captcha.strip()
        captcha=captcha.replace(' ','')
        return captcha

    def get_table_data(self,element:Union[Element_Info,WebElement],data_type:str='text')->List[List[str]]:
        """以二维数组返回表格每一行的每一列的数据[[row1][row2][colume1,clume2]]

        Args:
            element (Union[Element_Info,WebElement]): _description_
            data_type (str, optional): text-返回表格文本内容,html-返回表格html内容,webElement-返回表格元素. Defaults to 'text'.

        Returns:
            List[List[str]]: _description_
        """
        if isinstance(element, Element_Info):
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
        table_trs = web_element.find_elements(AppiumBy.TAG_NAME,'tr')
        try:
            for tr in table_trs:
                tr_data=[]
                tr_tds = tr.find_elements(AppiumBy.TAG_NAME,'td')
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
                print('获取表格内容异常:' + e.msg)
        return table_data

    def get_window_size(self)->dict:
        return self.driver.get_window_size()
    
    def get_window_rect(self)->dict:
        return self.driver.get_window_rect()

    def app_alert(self, platform_name:str,action_type:str='accept',button_label:str=None)->None:
        """"仅适用于app

        Args:
            platform_name (str): android、ios
            action_type (str, optional): accept、dismiss、getButtons. Defaults to 'accept'.
                                            getButtons只支持ios，返回所有按钮名
            button_label (str, optional): _description_. Defaults to None.
        """
        if action_type:
            action_type.lower()
        if platform_name:
            platform_name.lower()
        script=None
        script_arg={}
        if button_label:
            script_arg.update({'buttonLabel': button_label})
        if platform_name=='android':
            # 仅支持UiAutomator2
            #  该方法不是百分百可靠，https://github.com/appium/appium-uiautomator2-driver#platform-specific-extensions
            if action_type == 'accept':
                script = 'mobile:acceptAlert'
            elif action_type == 'dismiss':
                script = 'mobile:dismissAlert'
        elif platform_name=='ios':
            # 仅支持XCUITest
            script='mobile:alert'
            script_arg.update({'action':action_type})
        self.driver.execute_script(script,script_arg)

    def is_toast_visible(self, text:str, platform_name:str='android', automation_name:str='UiAutomator2', is_regexp:bool=False, wait_seconds:float=5)->bool:
        """仅支持Android

        Args:
            text (str): _description_
            platform_name (str, optional): android、ios. Defaults to 'android'.
            automation_name (str, optional):支持UiAutomator2、Espresso. Defaults to 'UiAutomator2'.
            is_regexp (bool, optional): 仅当automation_nameEspresso时有效. Defaults to False.
            wait_seconds (float, optional): _description_. Defaults to 5.

        Returns:
            bool: _description_
        """
        if not text:
            return False
        if 'android' == platform_name.lower():
            if 'uiautomator2' == automation_name.lower():
                toast_element = Create_Element.create(AppiumBy.XPATH, ".//*[contains(@text,'%s')]" % text, None,
                                                     Wait_By.PRESENCE_OF_ELEMENT_LOCATED, wait_seconds=wait_seconds)
                try:
                    self.get_element(toast_element)
                    return True
                except:
                    return False
            elif 'espresso' == automation_name.lower():
                script_arg = {'text': text}
                if is_regexp:
                    script_arg.update({'isRegexp': True})
                script = 'mobile:isToastVisible'
                return self.driver.execute_script(script, script_arg)
        elif 'ios' == platform_name.lower():
            return False

    def get_geolocation(self)->dict:
        """返回定位信息,纬度/经度/高度

        Returns:
            dict: _description_
        """
        return self.driver.location

    def set_geolocation(self,latitude:float,longitude:float,altitude:float)->None:
        """设置定位信息

        Args:
            latitude (float): 纬度 -90 ~ 90
            longitude (float): 经度 ~180 ~ 180
            altitude (float): 高度
        """
        self.driver.set_location(latitude,longitude,altitude)
        
    def get_orientation(self)->str:
        """获得当前设备或者浏览器的方向

        Returns:
            str: _description_
        """
        return self.driver.orientation
    
    def set_orientation(self,orientation:str)->None:
        """_summary_

        Args:
            orientation (str): LANDSCAPE、PORTRAIT
        """
        self.driver.orientation=orientation

    def start_activity(self,package_name:str,activity_name:str)->None:
        """启动Android的activity

        Args:
            package_name (str): _description_
            activity_name (str): _description_
        """
        self.driver.start_activity(package_name,activity_name)

    def get_current_activity(self)->str:
        """获得Android的activity

        Returns:
            str: _description_
        """
        return self.driver.current_activity

    def get_current_package(self)->str:
        """获得Android的package

        Returns:
            str: _description_
        """
        return self.driver.current_package
    
    def get_app_strings(self,language: str = None, string_file: str = None)->Dict[str,str]:
        return self.driver.app_strings()

    def execute_javascript(self,script:str,*args)->None:
        self.driver.execute_script(script,*args)

    def install_app(self,file_path:str)->None:
        """_summary_

        Args:
            file_path (str): 与appium server在同服务器的本地安装包路径或者网络远程地址
        """
        if not file_path.startswith('http'):
            file_path=os.path.abspath(file_path)
        self.driver.install_app(file_path)

    def is_app_installed(self,bundle_id:str)->bool:
        """_summary_

        Args:
            bundle_id (str): iOS：bundleid，Android：package name

        Returns:
            bool: _description_
        """
        return self.driver.is_app_installed(bundle_id)

    def remove_app(self,app_id:str,keepData:bool=False,timeout:int=20000)->None:
        """_summary_

        Args:
            app_id (str): _description_
            keepData (bool, optional): 仅支持Android. Defaults to False.
            timeout (int, optional): 卸载超时时间. Defaults to 20000.
        """
        self.driver.remove_app(app_id,keepData=keepData,timeout=timeout)

    def launch_app(self)->None:
        self.driver.launch_app()

    def reset_app(self)->None:
        """Appium 2.0.0 即将废弃该功能；不支持Espresso

        Returns:
            _type_: _description_
        """
        return self.driver.reset()

    def close_app(self)->None:
        """不支持Espresso
        """
        self.driver.close_app()

    def background_app(self,seconds:int)->None:
        """后台运行

        Args:
            seconds (int): -1代表完全停用
        """
        self.driver.background_app(seconds)

    def activate_app(self,app_id:str)->None:
        """_summary_

        Args:
            app_id (str): IOS是bundleId，Android是Package名
        """
        self.driver.activate_app(app_id)

    def terminate_app(self,app_id:str,timeout:float=None)->None:
        """不支持IOS的UIAutomation驱动

        Args:
            app_id (str): IOS是bundleId，Android是Package名
            timeout (float, optional): 重试超时时间，仅支持Android. Defaults to None.
        """
        if timeout:
            self.driver.terminate_app(app_id,timeout=timeout)
        else:
            self.driver.terminate_app(app_id)

    def get_app_state(self,app_id:str)->int:
        """不支持IOS的UIAutomation驱动

        Args:
            app_id (str): IOS是bundleId，Android是Package名

        Returns:
            int: 0:未安装,1:不在运行,2:在后台运行或者挂起,3:在后台运行,4:在前台运行
        """
        return self.driver.query_app_state(app_id)

    def get_clipboard(self,content_type:str='plaintext')->Union[bytes,str]:
        """不支持IOS的UIAutomation驱动；IOS13+真机需要WebDriverAgentRunner运行于前台，才能获得剪切板内容
        
        Args:
            content_type (str, optional): plaintxt、image、url. Defaults to 'plaintext'. Android上仅支持'plaintext'

        Returns:
            Union[bytes,str]: _description_
        """
        return self.driver.get_clipboard(content_type)
    
    def get_clipboard_text(self)->str:
        """不支持IOS的UIAutomation驱动；IOS13+真机需要WebDriverAgentRunner运行于前台，才能获得剪切板内容

        Returns:
            str: _description_
        """
        return self.driver.get_clipboard_text()

    def set_clipboard(self,content:bytes,content_type:str='plaintext',label:str=None)->None:
        """不支持IOS的UIAutomation驱动；IOS15+真机需要WebDriverAgentRunner运行于前台，才能获得剪切板内容

        Args:
            content (bytes): _description_
            content_type (str): plaintxt、image、url. Defaults to 'plaintext'. Android上仅支持'plaintext'
            label (str): 仅支持Android. Defaults to None.
        """
        self.driver.set_clipboard(content,content_type,label)
    
    def set_clipboard_text(self,text:str,label:str=None)->None:
        """不支持IOS的UIAutomation驱动；IOS15+真机需要WebDriverAgentRunner运行于前台，才能获得剪切板内容

        Args:
            text (str): _description_
            label (str, optional): 仅支持Android. Defaults to None.
        """
        self.driver.set_clipboard_text(text,label)
        
    def get_log_types(self)->list:
        return self.driver.log_types
    
    def get_log(self,log_type:str)->str:
        return self.driver.get_log(log_type)

    def push_file_to_device(self,device_filePath:str,local_filePath:str,base64data:str)->None:
        """上传文件设备，如果local_filePath和base64data均有，则默认使用local_filePath

        Args:
            device_filePath (str): _description_
            local_filePath (str): _description_
            base64data (str): _description_
        """
        self.driver.push_file(device_filePath,base64data,local_filePath)

    def pull_file_from_device(self,device_filePath:str,local_filePath:str)->None:
        """从设备上下载文件

        Args:
            device_filePath (str): _description_
            local_filePath (str): _description_
        """
        data=self.driver.pull_file(device_filePath)
        with open(local_filePath,'wb') as f:
            f.write(base64.b64decode(data))
            f.close()

    def pull_file_folder(self,device_dirPath:str,local_zip_filePath:str)->None:
        data=self.driver.pull_folder(device_dirPath)
        with open(local_zip_filePath,'wb') as f:
            f.write(base64.b64decode(data))
            f.close()

    def shake_device(self)->None:
        """仅支持IOS,详见https://appium.io/docs/en/commands/device/interactions/shake/index.html
        """
        self.driver.shake()

    def lock_screen(self,seconds:int=None)->None:
        """	XCUITest不支持

        Args:
            seconds (int, optional): 小于等于0，则永久锁屏，除非调用unlock_screen。其他则锁屏对应秒数后自动解锁
        """
        self.driver.lock(seconds)

    def unlock_screen(self)->None:
        """仅支持Android
        """
        self.driver.unlock()
        
    def is_locked_screen(self)->bool:
        self.driver.rot
        return self.driver.is_locked()
    
    def rotate(self,x:float,y:float,radius:float,rotation:float,touchCount:int,duration:int)->None:
        """仅支持IOS的UIAutomation

        Args:
            x (float): 旋转手势中心的x坐标
            y (float): 旋转手势中心的y坐标
            radius (float): 旋转手势中心到外围的距离
            rotation (float): 旋转手势弧度（360度）
            touchCount (int): 用户用来做出指定手势的手指数。有效值为1到5
            duration (int): 旋转花费时长
        """
        params={'x':x,'y':y,'radius':radius,'rotation':rotation,'touchCount':touchCount,'duration':duration}
        self.doRequest.post_with_form('/session/%s/appium/device/rotate'%(self.session_id),params=ujson.dumps(params))

    def press_keycode(self,keycode:int)->None:
        """按键盘按键，仅支持Android
           对照表：https://developer.android.com/reference/android/view/KeyEvent.html 

        Args:
            keycode (int): 键盘上每个按键的ascii
        """
        self.driver.press_keycode(keycode)

    def long_press_keycode(self,keycode:int)->None:
        """长按键盘按键，仅支持Android

        Args:
            keycode (int): 键盘上每个按键的ascii
        """
        self.driver.long_press_keycode(keycode)

    def hide_keyboard(self,key_name:str=None, key:str=None, strategy:str=None)->None:
        """隐藏软键盘,ios需要指定key_name或strategy,Android无需参数

        Args:
            key_name (str, optional): _description_. Defaults to None.
            key (str, optional): _description_. Defaults to None.
            strategy (str, optional): 仅支持IOS的UIAutomation，取值：'press', 'pressKey', 'swipeDown', 'tapOut', 'tapOutside', 'default'
        """
        self.driver.hide_keyboard(key_name,key,strategy)
        
    def is_keyboard_shown(self)->bool:
        return self.driver.is_keyboard_shown()

    def toggle_airplane_mode(self)->None:
        """切换飞行模式(开启关闭),仅支持Android
        """
        self.doRequest.post_with_form('/session/'+self.session_id+'/appium/device/toggle_airplane_mode')

    def toggle_data(self)->None:
        """切换蜂窝数据模式(开启关闭),仅支持Android
        """
        self.doRequest.post_with_form('/session/'+self.session_id+'/appium/device/toggle_data')

    def toggle_wifi(self)->None:
        """切换wifi模式(开启关闭),仅支持Android；从Android Q开始已被限制，使用UI操作进行开启、关闭WiFi
        """
        self.driver.toggle_wifi()

    def toggle_location_services(self)->None:
        """切换定位服务模式(开启关闭),仅支持Android
        """
        self.driver.toggle_location_services()

    def get_performance_date(self,data_type:str,package_name:str,data_read_timeout:int=10)->List[List[str]]:
        """获得设备性能数据，仅支持Android

        Args:
            data_type (str): cpuinfo、batteryinfo、networkinfo、memoryinfo
            package_name (str, optional): _description_. Defaults to None.
            data_read_timeout (float, optional): _description_. Defaults to 10.

        Returns:
            List[List[str]]: _description_
        """
        if data_type in self.driver.get_performance_data_types():
            return self.driver.get_performance_data(package_name,data_type,data_read_timeout)
    
    def get_performance_data_types(self)->List:
        """仅支持Android

        Returns:
            List: _description_
        """
        return self.driver.get_performance_data_types()
    
    def get_system_bars(self)->Dict:
        """仅支持Android

        Returns:
            Dict: _description_
        """
        return self.driver.get_system_bars()
    
    def get_device_time(self,format:str='YYYY-MM-DD HH:mm:ss')->str:
        """获得设备时间

        Args:
            format (str, optional): _description_. Defaults to 'YYYY-MM-DD HH:mm:ss'.

        Returns:
            _type_: _description_
        """
        return self.driver.get_device_time(format)

    def get_display_density(self)->int:
        """仅支持Android

        Returns:
            int: _description_
        """
        return self.driver.get_display_density()
    
    def get_settings(self)->dict:
        """获得设备的设置

        Returns:
            dict: _description_
        """
        return self.driver.get_settings()
        
    def update_settings(self,settings:dict)->None:
        """相关设置项：https://appium.io/docs/en/advanced-concepts/settings/index.html

        Args:
            settings (dict): _description_
        """
        self.driver.update_settings(settings)

    def start_recording_screen(self)->None:
        """默认录制为3分钟,android最大只能3分钟,ios最大只能10分钟。如果录制产生的视频文件过大无法放到手机内存里会抛异常，所以尽量录制短视频
        """
        self.driver.start_recording_screen(forcedRestart=True)

    def stop_recording_screen(self,fileName:str='')->None:
        """停止录像并将视频附加到报告里

        Args:
            fileName (str, optional): _description_. Defaults to ''.
        """
        fileName = DateTimeTool.getNowTime('%Y%m%d%H%M%S%f_') + fileName
        data=self.driver.stop_recording_screen()
        allure.attach(name=fileName, body=base64.b64decode(data), attachment_type=allure.attachment_type.MP4)

    def get_element_location(self,element:Union[Element_Info,WebElement])->dict:
        """获得元素在屏幕的位置,x、y坐标为元素左上角

        Args:
            element (Union[Element_Info,WebElement]): _description_

        Returns:
            dict: _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.location

    def get_element_center_location(self,element:Union[Element_Info,WebElement])->dict:
        """获得元素中心的x、y坐标

        Args:
            element (Union[Element_Info,WebElement]): _description_

        Returns:
            dict: _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            rect=web_element.rect
            height=rect['height']
            width=rect['width']
            x=rect['x']
            y=rect['y']
            result_x=x+width/2
            result_y=y+height/2
            return {'x':result_x,'y':result_y}

    def touch_element_left_slide(self,element:Union[Element_Info,WebElement],start_x_percent:float=0.5,start_y_percent:float=0.5,
                                 duration:int=500,edge_type:str='element')->None:
        """通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的左边缘

        Args:
            element (Union[Element_Info,WebElement]): _description_
            start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 500.
            edge_type (str, optional): element:滑动到元素边缘,screen:滑动到屏幕边缘. Defaults to 'element'.
        """
        
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            rect=web_element.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width * start_x_percent
            start_y = y + height * start_y_percent
            if edge_type.lower()=='element':
                end_x=x+0.01
                end_y=y+height*0.5
            elif edge_type.lower()=='screen':
                end_x = 0+0.01
                end_y = self.window_size['height'] * 0.5
            else:
                end_x=start_x
                end_y=end_x
            self.driver.swipe(start_x=start_x,start_y=start_y,end_x=end_x,end_y=end_y,duration=duration)

    def touch_element_right_slide(self,element:Union[Element_Info,WebElement],start_x_percent:float=0.5,start_y_percent:float=0.5,
                                  duration:int=500,edge_type:str='element')->None:
        """通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的右边缘

        Args:
            element (Union[Element_Info,WebElement]): _description_
            start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 500.
            edge_type (str, optional): element:滑动到元素边缘,screen:滑动到屏幕边缘. Defaults to 'element'.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            rect=web_element.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width*start_x_percent
            start_y = y + height*start_y_percent
            if edge_type.lower()=='element':
                end_x = x + width*0.99
                end_y = y + height * 0.5
            elif edge_type.lower()=='screen':
                end_x = self.window_size['width'] * 0.99
                end_y = self.window_size['height'] * 0.5
            else:
                end_x=start_x
                end_y=end_x
            self.driver.swipe(start_x=start_x,start_y=start_y,end_x=end_x,end_y=end_y,duration=duration)

    def touch_element_up_slide(self,element:Union[Element_Info,WebElement],start_x_percent:float=0.5,start_y_percent:float=0.5,
                               duration:int=500,edge_type:str='element')->None:
        """通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的上边缘
        
        Args:
            element (Union[Element_Info,WebElement]): _description_
            start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 500.
            edge_type (str, optional): element:滑动到元素边缘,screen:滑动到屏幕边缘. Defaults to 'element'.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            rect=web_element.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width*start_x_percent
            start_y = y + height*start_y_percent
            if edge_type.lower()=='element':
                end_x = x + width * 0.5
                end_y = y+0.01
            elif edge_type.lower()=='screen':
                end_x = self.window_size['width'] * 0.5
                end_y = 0+0.01
            else:
                end_x=start_x
                end_y=end_x
            self.driver.swipe(start_x=start_x,start_y=start_y,end_x=end_x,end_y=end_y,duration=duration)

    def touch_element_down_slide(self,element:Union[Element_Info,WebElement],start_x_percent:float=0.5,start_y_percent:float=0.5,
                                 duration:int=500,edge_type:str='element')->None:
        """通过元素宽度、高度的百分比值的位置点击滑动到元素或者屏幕的下边缘

        Args:
            element (Union[Element_Info,WebElement]): _description_
            start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 500.
            edge_type (str, optional): element:滑动到元素边缘,screen:滑动到屏幕边缘. Defaults to 'element'.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            rect=web_element.rect
            height = rect['height']
            width = rect['width']
            x = rect['x']
            y = rect['y']
            start_x = x + width*start_x_percent
            start_y = y + height*start_y_percent
            if edge_type.lower()=='element':
                end_x = x + width * 0.5
                end_y = y + height*0.99
            elif edge_type.lower()=='screen':
                end_x = self.window_size['width'] * 0.5
                end_y = self.window_size['height'] * 0.99
            else:
                end_x=start_x
                end_y=end_x
            self.driver.swipe(start_x=start_x,start_y=start_y,end_x=end_x,end_y=end_y,duration=duration)

    def touch_a_element_to_another_element_slide(self,src_element:Union[Element_Info,WebElement],dst_element:Union[Element_Info,WebElement],
                                                 src_start_x_percent:float=0.5,src_start_y_percent:float=0.5,dst_end_x_percent:float=0.5,
                                                 dst_end_y_percent:float=0.5,duration:int=500)->None:
        """通过一个元素宽度、高度的百分比值的位置点击滑动到另一个元素宽度、高度的百分比值的位置

        Args:
            src_element (Union[Element_Info,WebElement]): 开始的元素
            dst_element (Union[Element_Info,WebElement]): 结束的元素
            src_start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            src_start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            dst_end_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            dst_end_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 500.
        """
        if src_start_x_percent>=1:
            src_start_x_percent=0.99
        if src_start_y_percent>=1:
            src_start_y_percent=0.99
        if dst_end_x_percent>=1:
            dst_end_x_percent=0.99
        if dst_end_y_percent>=1:
            dst_end_y_percent=0.99
        src_web_element=self._change_element_to_web_element_type(src_element)
        dst_web_element = self._change_element_to_web_element_type(dst_element)
        if src_web_element and dst_web_element:
            src_rect=src_web_element.rect
            src_height = src_rect['height']
            src_width = src_rect['width']
            src_x = src_rect['x']
            src_y = src_rect['y']
            dst_rect=dst_web_element.rect
            dst_height = dst_rect['height']
            dst_width = dst_rect['width']
            dst_x = dst_rect['x']
            dst_y = dst_rect['y']
            # 计算位置
            start_x=src_x+src_width*src_start_x_percent
            start_y=src_y+src_height*src_start_y_percent
            end_x=dst_x+dst_width*dst_end_x_percent
            end_y=dst_y+dst_height*dst_end_y_percent
            self.driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, duration=duration)

    def touch_a_element_move_to_another_element(self, src_element:Union[Element_Info,WebElement], dst_element:Union[Element_Info,WebElement],
                                                src_start_x_percent:float=0.5,src_start_y_percent:float=0.5,dst_end_x_percent:float=0.5,
                                                dst_end_y_percent=0.5,long_press:bool=True,duration:int=0)->None:
        """通过一个元素宽度、高度的百分比值的位置点击移动到另一个元素宽度、高度的百分比值的位置

        Args:
            src_element (Union[Element_Info,WebElement]): 开始的元素
            dst_element (Union[Element_Info,WebElement]): 结束的元素
            src_start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            src_start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            dst_end_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            dst_end_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            long_press (bool, optional): 是否长按. Defaults to True.
            duration (int, optional): 毫秒，耗时. Defaults to 0.
        """
        if src_start_x_percent >= 1:
            src_start_x_percent = 0.99
        if src_start_y_percent >= 1:
            src_start_y_percent = 0.99
        if dst_end_x_percent >= 1:
            dst_end_x_percent = 0.99
        if dst_end_y_percent >= 1:
            dst_end_y_percent = 0.99
        src_web_element = self._change_element_to_web_element_type(src_element)
        dst_web_element = self._change_element_to_web_element_type(dst_element)
        if src_web_element and dst_web_element:
            src_rect = src_web_element.rect
            src_height = src_rect['height']
            src_width = src_rect['width']
            src_x = src_rect['x']
            src_y = src_rect['y']
            dst_rect = dst_web_element.rect
            dst_height = dst_rect['height']
            dst_width = dst_rect['width']
            dst_x = dst_rect['x']
            dst_y = dst_rect['y']
            # 计算位置
            start_x = src_x + src_width * src_start_x_percent
            start_y = src_y + src_height * src_start_y_percent
            end_x = dst_x + dst_width * dst_end_x_percent
            end_y = dst_y + dst_height * dst_end_y_percent
            self.touch_move_to(start_x, start_y, end_x, end_y, long_press, duration)

    def touch_a_element_drag_to_another_element(self, src_element:Union[Element_Info,WebElement], dst_element:Union[Element_Info,WebElement],
                                                src_start_x_percent:float=0.5,src_start_y_percent:float=0.5,dst_end_x_percent:float=0.5,
                                                dst_end_y_percent:float=0.5, duration:float=0.5)->None:
        """
        【仅适用IOS】通过一个元素宽度、高度的百分比值的位置点击拖拽到另一个元素宽度、高度的百分比值的位置 

        Args:
            src_element (Union[Element_Info,WebElement]): 开始的元素
            dst_element (Union[Element_Info,WebElement]): 结束的元素
            src_start_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            src_start_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            dst_end_x_percent (float, optional): 相对元素宽度的百分比，范围0~1. Defaults to 0.5.
            dst_end_y_percent (float, optional): 相对元素高度的百分比，范围0~1. Defaults to 0.5.
            duration (float, optional): 毫秒. Defaults to 0.5.
        """
        if src_start_x_percent >= 1:
            src_start_x_percent = 0.99
        if src_start_y_percent >= 1:
            src_start_y_percent = 0.99
        if dst_end_x_percent >= 1:
            dst_end_x_percent = 0.99
        if dst_end_y_percent >= 1:
            dst_end_y_percent = 0.99
        src_web_element = self._change_element_to_web_element_type(src_element)
        dst_web_element = self._change_element_to_web_element_type(dst_element)
        if src_web_element and dst_web_element:
            src_rect = src_web_element.rect
            src_height = src_rect['height']
            src_width = src_rect['width']
            src_x = src_rect['x']
            src_y = src_rect['y']
            dst_rect = dst_web_element.rect
            dst_height = dst_rect['height']
            dst_width = dst_rect['width']
            dst_x = dst_rect['x']
            dst_y = dst_rect['y']
            # 计算位置
            start_x = src_x + src_width * src_start_x_percent
            start_y = src_y + src_height * src_start_y_percent
            end_x = dst_x + dst_width * dst_end_x_percent
            end_y = dst_y + dst_height * dst_end_y_percent
            self.driver.execute_script("mobile:dragFromToForDuration",
                                        {"duration": duration, "elementId": None, "fromX": start_x, "fromY": start_y,
                                         "toX": end_x, "toY": end_y})

    def get_element_size_in_pixels(self,element:Union[Element_Info,WebElement])->dict:
        """返回元素的像素大小

        Args:
            element (Union[Element_Info,WebElement]): _description_

        Returns:
            dict: _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.size
        
    def get_element_rect(self,element:Union[Element_Info,WebElement])->dict:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.rect
    
    def get_element_css_property_value(self,element:Union[Element_Info,WebElement],css_property_name:str)->str:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.value_of_css_property(css_property_name)
        
    def get_location_in_view(self,element:Union[Element_Info,WebElement])->dict:
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            return web_element.location_in_view

    def get_all_contexts(self)->List[str]:
        """获得能够自动化测所有上下文(混合应用中的原生应用和web应用)

        Returns:
            _type_: _description_
        """
        return self.driver.contexts

    def get_current_context(self)->str:
        """获得当前appium中正在运行的上下文(混合应用中的原生应用和web应用)

        Returns:
            _type_: _description_
        """
        return self.driver.current_context

    def switch_context(self,context_name:str)->None:
        """切换上下文(混合应用中的原生应用和web应用)

        Args:
            context_name (str): _description_
        """
        context={}
        context.update({'name':context_name})
        self.doRequest.post_with_form('/session/'+self.session_id+'/context',params=ujson.dumps(context))

    def mouse_move_to(self,element:Union[Element_Info,WebElement],xoffset:int=0,yoffset:int=0)->None:
        """移动鼠标到指定位置(仅适用于Windows、mac)
        1、如果xoffset和yoffset都为0,则鼠标移动到指定元素的左上角
        2、如果element、xoffset和yoffset都不为0,则根据元素的左上角做x和y的偏移移动鼠标

        Args:
            element (Union[Element_Info,WebElement]): _description_
            xoffset (int, optional): _description_. Defaults to 0.
            yoffset (int, optional): _description_. Defaults to 0.
        """
        web_element=self._change_element_to_web_element_type(element)
        if element:
            actions = ActionChains(self.driver)
            if xoffset and yoffset:
                actions.move_to_element_with_offset(web_element,xoffset,yoffset)
            actions.move_to_element(web_element)
            actions.perform()

    def mouse_click(self)->None:
        """点击鼠标当前位置(仅适用于Windows、mac)
        """
        actions = ActionChains(self.driver)
        actions.click()
        actions.perform()

    def mouse_double_click(self)->None:
        """双击鼠标当前位置(仅适用于Windows、mac)
        """
        actions = ActionChains(self.driver)
        actions.double_click()
        actions.perform()

    def mouse_click_and_hold(self)->None:
        """长按鼠标(仅适用于Windows、mac)
        """
        actions = ActionChains(self.driver)
        actions.click_and_hold()
        actions.perform()

    def mouse_release_click_and_hold(self)->None:
        """停止鼠标长按(仅适用于Windows、mac)
        """
        actions = ActionChains(self.driver)
        actions.release()
        actions.perform()

    def touch_move_to(self,start_x:int,start_y:int,end_x:int,end_y:int,long_press=True,duration:int=0)->None:
        """点击从一个点移动到另外一个点

        Args:
            start_x (int): _description_
            start_y (int): _description_
            end_x (int): _description_
            end_y (int): _description_
            long_press (bool, optional): 是否长按. Defaults to True.
            duration (int, optional): 毫秒，为0时不会出现惯性滑动. Defaults to 0.
        """
        
        if long_press:
            action = TouchAction(self.driver)
            action.long_press(x=start_x,y=start_y,duration=duration).move_to(x=end_x,y=end_y).release().perform()
        else:
            actions = TouchAction(self.driver)
            actions.press(x=start_x, y=start_y).wait(duration)
            actions.move_to(x=end_x, y=end_y)
            actions.perform()
            
    def tap(self,x:int,y:int,duration:int=0)->None:
        """点击坐标

        Args:
            x (int): _description_
            y (int): _description_
            duration (int, optional): 毫秒. Defaults to 0.
        """
        self.driver.tap([(x,y)],duration)

    def touch_tap(self,element:Union[Element_Info,WebElement],xoffset:int=None,yoffset:int=None,count:int=1,is_perfrom:bool=True)->TouchAction:
        """触屏点击
        1、如果xoffset和yoffset都None,则在指定元素的正中间进行点击
        2、如果element、xoffset和yoffset都不为None,则根据元素的左上角做x和y的偏移然后进行点击

        Args:
            element (Union[Element_Info,WebElement]): _description_
            xoffset (int, optional): _description_. Defaults to None.
            yoffset (int, optional): _description_. Defaults to None.
            count (int, optional): 点击次数. Defaults to 1.
            is_perfrom (bool, optional): 是否马上执行动作,不执行可以返回动作给多点触控执行. Defaults to True.

        Returns:
            TouchAction: _description_
        """
        web_element=self._change_element_to_web_element_type(element)
        if web_element:
            actions=TouchAction(self.driver)
            actions.tap(web_element,xoffset,yoffset,count)
            if is_perfrom:
                actions.perform()
            return actions

    def touch_long_press(self,element:Union[Element_Info,WebElement],xoffset:int=None,yoffset:int=None,duration:int=1000,
                         is_perfrom=True)->TouchAction:
        """触屏长按
        1、如果xoffset和yoffset都None,则在指定元素的正中间进行长按
        2、如果element、xoffset和yoffset都不为None,则根据元素的左上角做x和y的偏移然后进行长按

        Args:
            element (Union[Element_Info,WebElement]): _description_
            xoffset (int, optional): _description_. Defaults to None.
            yoffset (int, optional): _description_. Defaults to None.
            duration (int, optional): 毫秒. Defaults to 1000.
            is_perfrom (bool, optional): 是否马上执行动作,不执行可以返回动作给多点触控执行. Defaults to True.

        Returns:
            TouchAction: _description_
        """
        web_element = self._change_element_to_web_element_type(element)
        if web_element:
            actions = TouchAction(self.driver)
            actions.long_press(web_element,xoffset,yoffset,duration)
            if is_perfrom:
                actions.perform()
            return actions

    def multi_touch_actions_perform(self,touch_actions:List[TouchAction])->None:
        """多点触控执行

        Args:
            touch_actions (List[TouchAction]): _description_
        """
        multiActions=MultiAction(self.driver)
        multiActions.add(*touch_actions)
        multiActions.perform()

    def touch_slide(self,start_element:Union[Element_Info,WebElement]=None,start_x:int=0, start_y:int=0, end_element:Union[Element_Info,WebElement]=None,
                    end_x:int=0, end_y:int=0, duration:int=0)->None:
        """
        滑动屏幕,在指定时间内从一个位置滑动到另外一个位置
        1、如果start_element不为None,则从元素的中间位置开始滑动
        2、如果end_element不为None,滑动结束到元素的中间位置

        Args:
            start_element (Union[Element_Info,WebElement], optional): _description_. Defaults to None.
            start_x (int, optional): _description_. Defaults to 0.
            start_y (int, optional): _description_. Defaults to 0.
            end_element (Union[Element_Info,WebElement], optional): _description_. Defaults to None.
            end_x (int, optional): _description_. Defaults to 0.
            end_y (int, optional): _description_. Defaults to 0.
            duration (int, optional): 毫秒. Defaults to 0.
        """
        start_web_element=self._change_element_to_web_element_type(start_element)
        end_web_element=self._change_element_to_web_element_type(end_element)
        if start_web_element:
            start_web_element_location=self.get_element_location(start_web_element)
            start_x=start_web_element_location['x']
            start_y=start_web_element_location['y']
        if end_web_element:
            end_web_element_location=self.get_element_location(end_web_element)
            end_x=end_web_element_location['x']
            end_y=end_web_element_location['y']
        self.driver.swipe(start_x,start_y,end_x,end_y,duration)

    def touch_left_slide(self,start_x_percent:float=0.5,start_y_percent:float=0.5,duration:int=500)->None:
        """
        通过屏幕宽度、高度的百分比值的位置点击滑动到元素的左边缘

        Args:
            start_x_percent (float, optional): 相对屏幕宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对屏幕高度的百分比，范围0~1. Defaults to 0.5.
            duration (int, optional): 毫秒. Defaults to 500.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        start_x=self.window_size['width']*start_x_percent
        start_y=self.window_size['height']*start_y_percent
        end_x=0
        end_y=self.window_size['height']*0.5
        self.driver.swipe(start_x,start_y,end_x,end_y,duration)

    def touch_right_slide(self,start_x_percent:float=0.5,start_y_percent:float=0.5,duration:int=500)->None:
        """通过屏幕宽度、高度的百分比值的位置点击滑动到元素的右边缘

        Args:
            start_x_percent (float, optional): 相对屏幕宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对屏幕高度的百分比，范围0~1. Defaults to 0.5.
            duration (int, optional): 毫秒. Defaults to 500.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        start_x=self.window_size['width']*start_x_percent
        start_y=self.window_size['height']*start_y_percent
        end_x=self.window_size['width']*0.99
        end_y=self.window_size['height']*0.5
        self.driver.swipe(start_x,start_y,end_x,end_y,duration)

    def touch_up_slide(self,start_x_percent:float=0.5,start_y_percent:float=0.5,duration:int=500)->None:
        """通过屏幕宽度、高度的百分比值的位置点击滑动到元素的上边缘

        Args:
            start_x_percent (float, optional): 相对屏幕宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对屏幕高度的百分比，范围0~1. Defaults to 0.5.
            duration (int, optional): 毫秒. Defaults to 500.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        start_x=self.window_size['width']*start_x_percent
        start_y=self.window_size['height']*start_y_percent
        end_x=self.window_size['width']*0.5
        end_y=0
        self.driver.swipe(start_x,start_y,end_x,end_y,duration)

    def touch_down_slide(self,start_x_percent:float=0.5,start_y_percent:float=0.5,duration:int=500)->None:
        """通过屏幕宽度、高度的百分比值的位置点击滑动到元素的下边缘

        Args:
            start_x_percent (float, optional): 相对屏幕宽度的百分比，范围0~1. Defaults to 0.5.
            start_y_percent (float, optional): 相对屏幕高度的百分比，范围0~1. Defaults to 0.5.
            duration (int, optional): _description_. Defaults to 500.
        """
        if start_x_percent>=1:
            start_x_percent=0.99
        if start_y_percent>=1:
            start_y_percent=0.99
        start_x=self.window_size['width']*start_x_percent
        start_y=self.window_size['height']*start_y_percent
        end_x=self.window_size['width']*0.5
        end_y=self.window_size['height']*0.99
        self.driver.swipe(start_x,start_y,end_x,end_y,duration)

    def get_element(self,element:Element_Info)->WebElement:
        """定位单个元素

        Args:
            element (Element_Info): _description_

        Returns:
            WebElement: _description_
        """
        web_element=None
        locator_type=element.locator_type
        locator_value=element.locator_value
        wait_type = element.wait_type
        wait_seconds = element.wait_seconds
        wait_expected_value = element.wait_expected_value
        

        # 查找元素,为了保证元素被定位,都进行显式等待,部分返回并非是WebElement对象
        # 相对位置定位方式【appium暂不支持】
        # relative_element = element.relative_element
        # relative_type = element.relative_type
        # if relative_element and relative_type:
        #     tmp_element=element
        #     tmp_element.relative_element=None
        #     tmp_element.relative_type=None
        #     tmp_web_element=self.get_element(tmp_element)
        #     if relative_type == 'above':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).above(tmp_web_element)
        #     elif relative_type == 'below':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).below(tmp_web_element)
        #     elif relative_type == 'to_left_of':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_left_of(tmp_web_element)
        #     elif relative_type == 'to_right_of':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_right_of(tmp_web_element)
        #     elif relative_type == 'near':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).near(tmp_web_element)
        #     else:
        #         relative_locattor={}
        #     web_element=self.driver.find_element(relative_locattor)
        #     return web_element
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
        return web_element

    def get_elements(self,element:Element_Info)->List[WebElement]:
        """定位多个元素

        Args:
            element (Element_Info): _description_

        Returns:
            List[WebElement]: _description_
        """
        web_elements=None
        locator_type=element.locator_type
        locator_value=element.locator_value
        wait_type = element.wait_type
        wait_seconds = element.wait_seconds
        

        # 查找元素,为了保证元素被定位,都进行显式等待,部分返回并非是WebElement对象
        # 相对位置定位方式
        # 相对位置定位方式【appium暂不支持】
        # relative_element = element.relative_element
        # relative_type = element.relative_type
        # if relative_element and relative_type:
        #     tmp_element=element
        #     tmp_element.relative_element=None
        #     tmp_element.relative_type=None
        #     tmp_web_element=self.get_element(tmp_element)
        #     if relative_type == 'above':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).above(tmp_web_element)
        #     elif relative_type == 'below':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).below(tmp_web_element)
        #     elif relative_type == 'to_left_of':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_left_of(tmp_web_element)
        #     elif relative_type == 'to_right_of':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).to_right_of(tmp_web_element)
        #     elif relative_type == 'near':
        #         relative_locattor=locate_with(relative_element.locator_type,relative_element.locator_value).near(tmp_web_element)
        #     else:
        #         relative_locattor={}
        #     web_elements=self.driver.find_elements(relative_locattor)
        #     return web_elements
        # 状态定位方式
        if wait_type == Wait_By.PRESENCE_OF_ALL_ELEMENTS_LOCATED:
            web_elements = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.presence_of_all_elements_located((locator_type, locator_value)))
        elif wait_type == Wait_By.VISIBILITY_OF_ALL_ELEMENTS_LOCATED:
            web_elements = WebDriverWait(self.driver, wait_seconds).until(expected_conditions.visibility_of_all_elements_located((locator_type,locator_value)))
        else:
        # 常规定位方式
            web_elements=WebDriverWait(self.driver,wait_seconds).until(lambda driver:driver.find_elements(locator_type,locator_value))
        return web_elements

    def get_sub_element(self,parent_element:Union[Element_Info,WebElement],sub_element:Element_Info)->WebElement:
        """获得元素的单个子元素

        Args:
            parent_element (Union[Element_Info,WebElement]): _description_
            sub_element (Element_Info): _description_

        Returns:
            WebElement: _description_
        """
        web_element=self._change_element_to_web_element_type(parent_element)
        if not web_element:
            return None
        if not isinstance(sub_element,Element_Info):
            return None

        # 通过父元素查找子元素
        locator_type=sub_element.locator_type
        locator_value=sub_element.locator_value
        wait_seconds = sub_element.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        sub_web_element = WebDriverWait(web_element, wait_seconds).until(lambda web_element: web_element.find_element(locator_type,locator_value))
        return sub_web_element

    def get_sub_elements(self, parent_element:Union[Element_Info,WebElement], sub_element:Element_Info)->List[WebElement]:
        """获得元素的多个子元素

        Args:
            parent_element (Union[Element_Info,WebElement]): _description_
            sub_element (Element_Info): _description_

        Returns:
            List[WebElement]: _description_
        """
        web_element=self._change_element_to_web_element_type(parent_element)
        if not web_element:
            return None
        if not isinstance(sub_element,Element_Info):
            return None

        # 通过父元素查找多个子元素
        locator_type = sub_element.locator_type
        locator_value = sub_element.locator_value
        wait_seconds = sub_element.wait_seconds

        # 查找元素,为了保证元素被定位,都进行显式等待
        sub_web_elements = WebDriverWait(web_element, wait_seconds).until(lambda web_element: web_element.find_elements(locator_type,locator_value))
        return sub_web_elements

    def explicit_wait_page_title(self,element:Element_Info)->None:
        """
        仅适用于web
        显式等待页面title
        :param elementInfo:
        :return:
        """
        self.get_element(element)