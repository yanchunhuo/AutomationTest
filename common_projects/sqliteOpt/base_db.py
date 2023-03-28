#
# base_db.py
# @author yanchunhuo
# @description 
# @created 2022-08-04T09:52:09.525Z+08:00
# @last-modified 2023-03-28T13:14:23.295Z+08:00
# github https://github.com/yanchunhuo

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
        attrs=(obj.__dict__).copy()
        attrs.pop('_sa_instance_state')
        try:
            if order_by_columns:
                result_object=self.db_session.query(self.model).filter_by(**attrs).order_by(*order_by_columns).first()
            else:
                result_object=self.db_session.query(self.model).filter_by(**attrs).first()
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
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
        attrs=(obj.__dict__).copy()
        attrs.pop('_sa_instance_state')
        try:
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
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        return result_objects
    
    def add_object(self,obj:object):
        try:
            self.db_session.add(obj)
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        
    def add_objects(self, objs: list = []):
        try:
            self.db_session.bulk_save_objects(objs)
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        
    def delete_object(self,obj:object):
        attrs=(obj.__dict__).copy()
        attrs.pop('_sa_instance_state')
        try:
            num=self.db_session.query(self.model).filter_by(**attrs).delete()
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        return num
    
    def empty_table(self):
        try:
            num=self.db_session.query(self.model).delete()
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        return num
    
    def update_object(self,old_obj:object,new_obj):
        """变更的new_obj，如果需要将某个字段更新为Null，则设置字段值为'null'

        Args:
            old_obj (object): _description_
            new_obj (_type_): _description_
        """
        old_attrs=(old_obj.__dict__).copy()
        old_attrs.pop('_sa_instance_state')
        try:
            old_result_object=self.db_session.query(self.model).filter_by(**old_attrs).first()
            if old_result_object:
                for key in old_result_object.__dict__.keys():
                    if not key=='_sa_instance_state' and hasattr(new_obj,key):
                        key_new_value=getattr(new_obj,key)
                        if not key_new_value is None:
                            if key_new_value=='null'.lower():
                                key_new_value=None
                            setattr(old_result_object,key,key_new_value)
                self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        
    def update_objects(self,old_obj:object,new_obj):
        """变更的new_obj，如果需要将某个字段更新为Null，则设置字段值为'null'

        Args:
            old_obj (object): _description_
            new_obj (_type_): _description_
        """
        old_attrs=(old_obj.__dict__).copy()
        old_attrs.pop('_sa_instance_state')
        try:
            old_result_objects=self.db_session.query(self.model).filter_by(**old_attrs).all()
            for old_result_object in old_result_objects:
                for key in old_result_object.__dict__.keys():
                    if not key=='_sa_instance_state' and hasattr(new_obj,key):
                        key_new_value=getattr(new_obj,key)
                        if not key_new_value is None:
                            if key_new_value=='null'.lower():
                                key_new_value=None
                            setattr(old_result_object,key,key_new_value)
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise