# -*- coding:utf8 -*-
from base.app_ui.android.demoProject.app_ui_android_demoProject_client import APP_UI_Android_demoProject_Client
from page_objects.app_ui.android.demoProject.pages.startPage import StartPage
import pytest
class TestStartPage:
    def setup_class(self):
        self.demoProjectClient = APP_UI_Android_demoProject_Client()
        self.startPage=StartPage(self.demoProjectClient.appOperator)

    @pytest.fixture(autouse=True)
    def record_test_case_video(self):
        self.demoProjectClient.appOperator.start_recording_screen()
        yield self.record_test_case_video
        self.demoProjectClient.appOperator.stop_recording_screen()

    @pytest.fixture
    def fixture_test_click_start_btn(self):
        print('start......')
        yield self.fixture_test_click_start_btn
        print('end......')

    def test_click_start_btn(self,fixture_test_click_start_btn):
        self.startPage.click_start()

    def test_search_chinese(self):
        self.startPage.searh_city('大学')

    def test_search_en(self):
        self.startPage.searh_city('aaa')

    def test_choice_a_city(self):
        self.startPage.choice_a_city()

    def teardown_class(self):
        self.demoProjectClient.appOperator.reset_app()