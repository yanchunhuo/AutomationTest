# -*- coding:utf8 -*-
from base.app_ui.android.demoProject.app_ui_android_demoProject_client import APP_UI_Android_demoProject_Client
from page_objects.app_ui.android.demoProject.pages.startPage import StartPage
import pytest
import time

class TestIndexPage:
    def setup_class(self):
        self.demoProjectClient = APP_UI_Android_demoProject_Client()
        self.startPage=StartPage(self.demoProjectClient.appPerator)
        self.startPage.click_start()
        self.indexPage=self.startPage.choice_a_city()
        self.appPerator=self.demoProjectClient.appPerator

    @pytest.fixture(autouse=True)
    def record_test_case_video(self):
        self.demoProjectClient.appPerator.start_recording_screen()
        yield self.record_test_case_video
        self.demoProjectClient.appPerator.stop_recording_screen()

    @pytest.fixture
    def fixture_test_silde(self):
        print('start......')
        yield self.fixture_test_silde
        print('end......')

    def test_silde(self,fixture_test_silde):
        time.sleep(10)
        self.indexPage.index_left_silde()
        self.indexPage.index_right_silde()
        self.indexPage.index_up_silde()
        self.indexPage.index_down_silde()

    def teardown_class(self):
        self.demoProjectClient.appPerator.reset_app()