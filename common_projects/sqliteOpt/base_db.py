#
# base_db.py
# @author yanchunhuo
# @description 
# @created 2022-08-04T09:52:09.525Z+08:00
# @last-modified 2022-08-08T13:08:52.202Z+08:00
# github https://github.com/yanchunhuo

import copy

class Base_DB:
    def __init__(self,db_session,model) -> None:
        self.db_session=db_session
        self.model=model
    
    def filter_object(self,obj:object):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        result_object=self.db_session.query(self.model).filter_by(**attrs).first()
        return result_object

    def filter_objects(self,obj:object,page_index:int=None,page_size:int=None,):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        if page_index and page_size:
            result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                limit(page_size).offset((page_index-1)*page_size).all()
        else:
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