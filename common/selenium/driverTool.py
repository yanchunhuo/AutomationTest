#-*- coding:utf8 -*-
from base.read_web_ui_config import Read_WEB_UI_Config
from selenium import webdriver
from selenium.webdriver.ie import webdriver as ie_webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.chrome.options import Options as Chrome_Options

class DriverTool:

    @classmethod
    def get_driver(cls,selenium_hub,browser_type):
        driver=None
        browser_type=browser_type.lower()
        download_file_content_types = "application/octet-stream,application/vnd.ms-excel,text/csv,application/zip,application/binary"

        if browser_type=='ie':
            opt = ie_webdriver.Options()
            opt.force_create_process_api = True
            opt.ensure_clean_session = True
            opt.add_argument('-private')
            ie_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            ie_capabilities.update(opt.to_capabilities())
            driver = webdriver.Remote(selenium_hub, desired_capabilities=ie_capabilities)
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
            driver = webdriver.Remote(selenium_hub, webdriver.DesiredCapabilities.FIREFOX.copy(),options=firefox_options)
        elif browser_type=='chrome':
            chrome_options=Chrome_Options()
            prefs={'download.default_directory':Read_WEB_UI_Config().web_ui_config.download_dir,'profile.default_content_settings.popups':0}
            chrome_options.add_experimental_option('prefs',prefs)
            if Read_WEB_UI_Config().web_ui_config.is_chrome_headless.lower()=='true':
                chrome_options.add_argument('--headless')
            driver = webdriver.Remote(selenium_hub, webdriver.DesiredCapabilities.CHROME.copy(),options=chrome_options)
        else:
            return driver
        driver.maximize_window()
        driver.delete_all_cookies()
        return driver