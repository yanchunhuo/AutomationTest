# -*- coding:utf-8 -*-
class WEB_UI_Config:
    def __init__(self):
        self.selenium_hub=None
        self.test_workers=None
        self.test_browsers=[]
        self.current_browser=None
        self.download_dir = None
        self.is_chrome_headless = None
        self.is_firefox_headless = None