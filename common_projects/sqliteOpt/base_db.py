#
# base_db.py
# @author yanchunhuo
# @description 
# @created 2022-08-04T09:52:09.525Z+08:00
# @last-modified 2022-08-09T10:22:25.053Z+08:00
# github https://github.com/yanchunhuo

from sqlalchemy import desc
import copy

class Base_DB:
    def __init__(self,db_session,model) -> None:
        self.db_session=db_session
        self.model=model
    
    def filter_object(self,obj:object,order_by_column:str=None,is_desc=False):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        if order_by_column and is_desc:
            result_object=self.db_session.query(self.model).filter_by(**attrs).order_by(desc(order_by_column)).first()
        elif order_by_column and not is_desc:
            result_object=self.db_session.query(self.model).filter_by(**attrs).order_by(order_by_column).first()
        elif not order_by_column:
            result_object=self.db_session.query(self.model).filter_by(**attrs).first()
        return result_object

    def filter_objects(self,obj:object,page_index:int=None,page_size:int=None,order_by_column:str=None,is_desc=None):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        if page_index and page_size:
            if order_by_column and is_desc:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                    order_by(desc(order_by_column)).limit(page_size).offset((page_index-1)*page_size).all()
            elif order_by_column and not is_desc:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                    order_by(order_by_column).limit(page_size).offset((page_index-1)*page_size).all()
            elif not order_by_column:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                    limit(page_size).offset((page_index-1)*page_size).all()
        else:
            if order_by_column and is_desc:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).order_by(desc(order_by_column)).all()
            elif order_by_column and not is_desc:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).order_by(order_by_column).all()
            elif not order_by_column:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).all()
        return result_objects
    
    def add_object(self,obj:object):
        self.db_session.add(obj)
        self.db_session.commit()
        
    def add_object(self,objs:list=[]):
        self.db_session.add_all(objs)
        self.commit()
        
    def delete_object(self,obj:object):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        num=self.db_session.query(self.model).filter_by(**attrs).delete()
        self.db_session.commit()
        return num
    
    def empty_table(self):
        num=self.db_session.query(self.model).delete()
        self.db_session.commit()
        return num
    
    def update_object(self,old_obj:object,new_obj):
        old_attrs=old_obj.__dict__
        old_attrs.pop('_sa_instance_state')
        old_result_object=self.db_session.query(self.model).filter_by(**old_attrs).first()
        if old_result_object:
            old_result_object=copy.copy(new_obj)
            self.db_session.commit()