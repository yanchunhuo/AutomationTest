#
# base_db.py
# @author yanchunhuo
# @description 
# @created 2022-08-04T09:52:09.525Z+08:00
# @last-modified 2022-08-04T10:34:56.676Z+08:00
# github https://github.com/yanchunhuo

class Base_DB:
    def __init__(self,db_session,model) -> None:
        self.db_session=db_session
        self.model=model
    
    def filter_object(self,obj:object):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        result_object=self.db_session.query(self.model).filter_by(**attrs).first()
        return result_object

    def filter_objects(self,obj:object):
        attrs=obj.__dict__
        attrs.pop('_sa_instance_state')
        result_objects=self.db_session.query(self.model).filter_by(**attrs).all()
        return result_objects