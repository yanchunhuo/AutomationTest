#
# user.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:40:40.521Z+08:00
# @last-modified 2022-08-04T10:34:43.403Z+08:00
# github https://github.com/yanchunhuo

from base.sqliteOpt.demoProject.demoProject_sessions import DemoProject_Sessions
from common_projects.sqliteOpt.base_db import Base_DB
from models.demoProject.user import User

class User_DB(Base_DB):
    def __init__(self) -> None:
        self.db_demoProject_session=DemoProject_Sessions().db_demoProject_session
        super(User_DB,self).__init__(self.db_demoProject_session,User)
        
    def get_user_by_name(self,user_name):
        users=self.db_demoProject_session.query(User).filter(User.name==user_name).all()
        return users