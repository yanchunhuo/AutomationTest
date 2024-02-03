#
# user.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:40:40.521Z+08:00
# @last-modified 2024-02-03T11:36:38.685Z+08:00
# github https://github.com/yanchunhuo

from base.sqlite_opt.demoProject.demoProject_sessions import DemoProject_Sessions
from common_projects.sqlite_opt.base_db import BaseDB
from models.demoProject.user import User

class User_DB(BaseDB):
    def __init__(self) -> None:
        self.db_demoProject_session=DemoProject_Sessions().db_demoProject_session
        super(User_DB,self).__init__(self.db_demoProject_session,User)