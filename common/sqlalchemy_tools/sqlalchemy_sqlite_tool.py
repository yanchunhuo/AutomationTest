#
# sqlalchemy_sqlite_tool.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:11:48.078Z+08:00
# @last-modified 2024-02-03T11:44:47.652Z+08:00
# github https://github.com/yanchunhuo

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

class SQLAlchemySqliteTool:
    def __init__(self,file_path,encoding='utf8',echo=False) -> None:
        self.url='sqlite:///%s'%(file_path)
        self.encoding=encoding
        self.echo=echo
        
    def get_session(self,pool_size:int=50):
        engine=create_engine(url=self.url,encoding=self.encoding,echo=self.echo,pool_size=pool_size, max_overflow=0)
        # 线程安全
        return scoped_session(sessionmaker(bind=engine))