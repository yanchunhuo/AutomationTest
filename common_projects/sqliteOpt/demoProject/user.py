#
# user.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:40:40.521Z+08:00
# @last-modified 2022-07-25T19:57:16.904Z+08:00
# github https://github.com/yanchunhuo

from base.sqliteOpt.demoProject.demoProject_sessions import DemoProject_Sessions
from models.demoProject.user import User as User_Model

class User:
    def __init__(self) -> None:
        self.db_demoProject_session=DemoProject_Sessions().db_demoProject_session
        
    def get_user_by_name(self,user_name):
        users=self.db_demoProject_session.query(User_Model).filter(User_Model.name==user_name).all()
        return users