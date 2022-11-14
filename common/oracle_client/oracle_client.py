#
# oracle_client.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2018-01-19T14:15:32.262Z+08:00
# @last-modified 2022-11-14T14:19:29.600Z+08:00
#

##### 暂未升级库，暂不可用，基于cx_Oracle 6.3.1版本
# import cx_Oracle

# class Oracle_Client:
#     def __init__(self,host,port,username,password,dbname):
#         self._dsn=cx_Oracle.makedsn(host,port,dbname)
#         self._conn=cx_Oracle.connect(user=username,password=password,dsn=self._dsn)
#         self._cursor=self._conn.cursor()

#     def update_sql(self, sql):
#         """
#         增、删操作
#         :param sql:
#         :return:
#         """
#         try:
#             self._cursor.execute(sql)
#             self._conn.commit()
#         except Exception as e:
#             print(e.args.__str__())
#             self._conn.rollback()

#     def query_sql(self,sql):
#         result=None
#         try:
#             self._cursor.execute(sql)
#             result=self._cursor.fetchall()
#             self._conn.commit()
#         except Exception as e:
#             print(e.args.__str__())
#             self._conn.rollback()
#         return result

#     def execute_many(self, query, values):
#         """
#         :param query: insert into table(field1,field2) values(:1,:2)
#         :param values: [(field1_value1,field2_value2),(field1_value3,field2_value4)]
#         :return:
#         """
#         try:
#             self._cursor.executemany(query, values)
#             self._conn.commit()
#         except Exception as e:
#             print(e.args.__str__())
#             self._conn.rollback()

#     def close_all(self):
#         self._cursor.close()
#         self._conn.close()