#
# user.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:51:16.167Z+08:00
# @last-modified 2022-07-25T19:56:52.705Z+08:00
# github https://github.com/yanchunhuo


from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    age = Column(Integer)
    sex = Column(Integer)
    phone = Column(Text)
    address = Column(Text)
