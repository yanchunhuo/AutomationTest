#
# sqlalchemy_mysql_tool.py
# @author yanchunhuo
# @description 
# @created 2022-07-21T18:07:28.086Z+08:00
# @last-modified 2022-07-25T19:58:02.887Z+08:00
# github https://github.com/yanchunhuo

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

class SQLAlchemy_Mysql_Tool:
    def __init__(self,host:str=None,port:str=None,username:str=None,password:str=None,db:str=None,
                 driver_type='pymysql',encoding='utf8',echo=False) -> None:
        self.url='mysql+%s://%s:%s@%s:%s/%s'%(driver_type,username,password,host,str(port),db)
        self.encoding=encoding
        self.echo=echo
        
    def get_session(self):
        engine=create_engine(url=self.url,encoding=self.encoding,echo=self.echo)
        # 线程安全
        return scoped_session(sessionmaker(bind=engine))