#
# driver_tool.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T13:47:34.673Z+08:00
# @last-modified 2024-02-03T10:53:56.164Z+08:00
#

from base.read_web_ui_config import ReadWebUiConfig
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Chrome_Options
from selenium.webdriver.edge.options import Options as Edge_Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.options import Options as Safari_Options
import os

class DriverTool:
    
    @classmethod
    def get_driver(cls,selenium_hub:str,browser_type:str)->WebDriver:
        """_summary_

        Args:
            selenium_hub (str): _description_
            browser_type (str): edge、firefox、chrome、safari

        Returns:
            WebDriver: _description_
        """
        cls.web_ui_config=ReadWebUiConfig().web_ui_config
        driver=None
        browser_type=browser_type.lower()
        download_file_content_types = "application/octet-stream,application/vnd.ms-excel,text/csv,application/zip,application/binary"

        if browser_type=='edge':
            edge_options = Edge_Options()
            if cls.web_ui_config['browser']['is_edge_headless']:
                edge_options.add_argument('--headless')
            edge_options.accept_insecure_certs=True
            if cls.web_ui_config['browser']['proxy_host'] and cls.web_ui_config['browser']['proxy_port']:
                edge_options.add_argument('--proxy-server=http://%s:%s'%(cls.web_ui_config['browser']['proxy_host'],cls.web_ui_config['browser']['proxy_port']))
            driver = webdriver.Remote(selenium_hub,webdriver.DesiredCapabilities.EDGE.copy(),options=edge_options)
        elif browser_type=='firefox':
            firefox_profile=FirefoxProfile()
            # firefox_profile参数可以在火狐浏览器中访问about:config进行查看
            firefox_profile.set_preference('browser.download.folderList',2) # 0是桌面;1是“我的下载”;2是自定义
            firefox_profile.set_preference('browser.download.dir',cls.web_ui_config['browser']['download_dir'])
            firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk',download_file_content_types)
            firefox_options = Firefox_Options()
            if cls.web_ui_config['browser']['is_firefox_headless']:
                firefox_options.add_argument('--headless')
            firefox_options.profile=firefox_profile
            firefox_options.accept_insecure_certs=True
            browser_profile=webdriver.DesiredCapabilities.FIREFOX.copy()
            if cls.web_ui_config['browser']['proxy_host'] and cls.web_ui_config['browser']['proxy_port']:
                PROXY='%s:%s'%(cls.web_ui_config['browser']['proxy_host'],cls.web_ui_config['browser']['proxy_port'])
                browser_profile['proxy']={
                    'httpProxy': PROXY,
                    'sslProxy': PROXY,
                    'proxyType': 'MANUAL'
                }
            driver = webdriver.Remote(selenium_hub, browser_profile,options=firefox_options)
        elif browser_type=='chrome':
            chrome_options=Chrome_Options()
            prefs={'download.default_directory':cls.web_ui_config['browser']['download_dir'],'profile.default_content_settings.popups':0}
            chrome_options.add_experimental_option('prefs',prefs)
            if cls.web_ui_config['browser']['is_chrome_headless']:
                chrome_options.add_argument('--headless')
            chrome_options.accept_insecure_certs=True
            if cls.web_ui_config['browser']['proxy_host'] and cls.web_ui_config['browser']['proxy_port']:
                chrome_options.add_argument('--proxy-server=http://%s:%s'%(cls.web_ui_config['browser']['proxy_host'],cls.web_ui_config['browser']['proxy_port']))
            driver = webdriver.Remote(selenium_hub, webdriver.DesiredCapabilities.CHROME.copy(),options=chrome_options)
        elif browser_type=='safari':
            safari_options=Safari_Options()
            safari_options.accept_insecure_certs=True
            driver = webdriver.Remote(selenium_hub,webdriver.DesiredCapabilities.SAFARI.copy(),options=safari_options)
        driver.maximize_window()
        # 将session_id存储起来，以便进行后续其他相关操作【此处可优化，不应在common内写死相关路径或代码】
        if not os.path.exists('output/tmp/web_ui/'):
            os.makedirs('output/tmp/web_ui/')
        with open('output/tmp/web_ui/driver_sessions_info','a+',encoding='utf-8') as f:
            f.write(driver.session_id)
            f.write('\n')
            f.close()
        return driver