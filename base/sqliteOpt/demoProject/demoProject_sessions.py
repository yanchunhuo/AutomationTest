#
# demoProject_sessions.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:32:07.806Z+08:00
# @last-modified 2022-07-25T19:58:23.123Z+08:00
# github https://github.com/yanchunhuo


from common.sqlalchemy_tools.sqlalchemy_sqlite_tool import SQLAlchemy_Sqlite_Tool

class DemoProject_Sessions(object):
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self,):
        if self.__inited is None:            
            self.db_demoProject_session=SQLAlchemy_Sqlite_Tool('models/demoProject/demoProject.db').get_session()
                        
        self.__inited = True
