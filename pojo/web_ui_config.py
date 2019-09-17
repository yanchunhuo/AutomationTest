# -*- coding:utf-8 -*-
class WEB_UI_Config:
    def __init__(self):
        self._selenium_hub=None
        self._test_workers=None
        self._test_browsers=[]
        self._current_browser=None
        self._download_dir = None
        self._is_chrome_headless = None
        self._is_firefox_headless = None

    @property
    def selenium_hub(self):
        return self._selenium_hub

    @selenium_hub.setter
    def selenium_hub(self,selenium_hub):
        self._selenium_hub=selenium_hub

    @property
    def test_workers(self):
        return self._test_workers

    @test_workers.setter
    def test_workers(self,test_workers):
        self._test_workers=test_workers

    @property
    def current_browser(self):
        return self._current_browser

    @current_browser.setter
    def current_browser(self,current_browser):
        self._current_browser=current_browser

    @property
    def download_dir(self):
        return self._download_dir

    @download_dir.setter
    def download_dir(self,download_dir):
        self._download_dir=download_dir

    @property
    def is_chrome_headless(self):
        return self._is_chrome_headless

    @is_chrome_headless.setter
    def is_chrome_headless(self, is_chrome_headless):
        self._is_chrome_headless = is_chrome_headless

    @property
    def is_firefox_headless(self):
        return self._is_firefox_headless

    @is_firefox_headless.setter
    def is_firefox_headless(self, is_firefox_headless):
        self._is_firefox_headless = is_firefox_headless