#
# base_db.py
# @author yanchunhuo
# @description 
# @created 2022-08-04T09:52:09.525Z+08:00
# @last-modified 2022-08-09T14:06:38.203Z+08:00
# github https://github.com/yanchunhuo
import copy

class Base_DB:
    def __init__(self,db_session,model) -> None:
        self.db_session=db_session
        self.model=model
    
    def filter_object(self,obj:object,order_by_columns:list=None):
        """_summary_

        Args:
            obj (object): _description_
            order_by_columns (list, optional): 
                数据库字段名，如需降序使用desc方法，例：
                from sqlalchemy import desc                
                ['AGENT_ID',desc('ROLE_ID')]. Defaults to None.

        Returns:
            _type_: _description_
        """
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        if order_by_columns:
            result_object=self.db_session.query(self.model).filter_by(**attrs).order_by(*order_by_columns).first()
        else:
            result_object=self.db_session.query(self.model).filter_by(**attrs).first()
        return result_object

    def filter_objects(self,obj:object,page_index:int=None,page_size:int=None,order_by_columns:list=None):
        """_summary_

        Args:
            obj (object): _description_
            page_index (int, optional): _description_. Defaults to None.
            page_size (int, optional): _description_. Defaults to None.
            order_by_columns (list, optional): 
                数据库字段名，如需降序使用desc方法，例：
                from sqlalchemy import desc                
                ['AGENT_ID',desc('ROLE_ID')]. Defaults to None.

        Returns:
            _type_: _description_
        """
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        if page_index and page_size:
            if order_by_columns:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                    order_by(*order_by_columns).limit(page_size).offset((page_index-1)*page_size).all()
            else:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).\
                    limit(page_size).offset((page_index-1)*page_size).all()
        else:
            if order_by_columns:
                result_objects=self.db_session.query(self.model).filter_by(**attrs).order_by(*order_by_columns).all()
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