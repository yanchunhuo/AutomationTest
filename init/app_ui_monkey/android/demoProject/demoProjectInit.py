#
# demoProjectInit.py
# @author yanchunhuo
# @description 
# @created 2021-05-20T17:21:12.247Z+08:00
# @last-modified 2021-05-20T18:04:18.506Z+08:00
# github https://github.com/yanchunhuo

class DemoProjectInit:
    def init(self,is_init=False):
        if not is_init:
            return
        #每次测试前先清除上次构造的数据
        self._deinit()
        #初始化必要的数据，如在数据库中构建多种类型的账号，
        pass

    def _deinit(self):
        #清除构造的数据
        pass