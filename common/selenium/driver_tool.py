#
# driver_tool.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.673Z+08:00
# @last-modified 2022-11-22T16:32:38.356Z+08:00
#

from base.read_web_ui_config import Read_WEB_UI_Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.edge.options import Options as Edge_Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.options import Options as Safari_Options
import os

class Driver_Tool:
    
    @classmethod
    def get_driver(cls,selenium_hub:str,browser_type:str)->WebDriver:
        """_summary_

        Args:
            selenium_hub (str): _description_
            browser_type (str): edge、firefox、chrome、safari

        Returns:
            WebDriver: _description_
        """
        driver=None
        browser_type=browser_type.lower()
        download_file_content_types = "application/octet-stream,application/vnd.ms-excel,text/csv,application/zip,application/binary"

        if browser_type=='edge':
            edge_options = Edge_Options()
            if Read_WEB_UI_Config().web_ui_config.is_edge_headless.lower()=='true':
                edge_options.add_argument('--headless')
            edge_options.accept_insecure_certs=True
            driver = webdriver.Remote(selenium_hub,webdriver.DesiredCapabilities.EDGE.copy(),options=edge_options)
        elif browser_type=='firefox':
            firefox_profile=FirefoxProfile()
            # firefox_profile参数可以在火狐浏览器中访问about:config进行查看
            firefox_profile.set_preference('browser.download.folderList',2) # 0是桌面;1是“我的下载”;2是自定义
            firefox_profile.set_preference('browser.download.dir',Read_WEB_UI_Config().web_ui_config.download_dir)
            firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk',download_file_content_types)
            firefox_options = Firefox_Options()
            if Read_WEB_UI_Config().web_ui_config.is_firefox_headless.lower()=='true':
                firefox_options.add_argument('--headless')
            firefox_options.profile=firefox_profile
            firefox_options.accept_insecure_certs=True
            driver = webdriver.Remote(selenium_hub, webdriver.DesiredCapabilities.FIREFOX.copy(),options=firefox_options)
        elif browser_type=='chrome':
            chrome_options=Chrome_Options()
            prefs={'download.default_directory':Read_WEB_UI_Config().web_ui_config.download_dir,'profile.default_content_settings.popups':0}
            chrome_options.add_experimental_option('prefs',prefs)
            if Read_WEB_UI_Config().web_ui_config.is_chrome_headless.lower()=='true':
                chrome_options.add_argument('--headless')
            chrome_options.accept_insecure_certs=True
            driver = webdriver.Remote(selenium_hub, webdriver.DesiredCapabilities.CHROME.copy(),options=chrome_options)
        elif browser_type=='safari':
            safari_options=Safari_Options()
            safari_options.accept_insecure_certs=True
            driver = webdriver.Remote(selenium_hub,webdriver.DesiredCapabilities.SAFARI.copy(),options=safari_options)
        driver.maximize_window()
        # 将session_id存储起来，以便进行后续其他相关操作【此处可优化，不应在common内写死相关路径或代码】
        if not os.path.exists('output/tmp/web_ui/'):
            os.mkdir('output/tmp/web_ui/')
        with open('output/tmp/web_ui/driver_sessions_info','a+',encoding='utf-8') as f:
            f.write(driver.session_id)
            f.write('\n')
            f.close()
        return driver