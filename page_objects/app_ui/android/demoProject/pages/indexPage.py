#-*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from page_objects.app_ui.android.demoProject.elements.indexPageElements import IndexPageElements

class IndexPage:
    def __init__(self,app_operator):
        self.app_operator=app_operator
        self._indexPageElement=IndexPageElements()


    def index_left_silde(self):
        self.app_operator.touch_left_slide()

    def index_right_silde(self):
        self.app_operator.touch_right_slide()

    def index_up_silde(self):
        self.app_operator.touch_up_slide()

    def index_down_silde(self):
        self.app_operator.touch_down_slide()