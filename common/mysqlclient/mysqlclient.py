#-*- coding:utf-8 -*-

import pymysql

class MysqlClient:
    def __init__(self,host,port,username,password,dbname,charset='utf8'):
        self._conn=pymysql.connect(host=host,port=int(port),user=username,passwd=password,db=dbname,charset=charset)
        self._cursor=self._conn.cursor()

    def executeSQL(self,sql):
        # try:
        # 为了避免连接被服务器关闭,检测进行重连
        self._conn.ping(reconnect=True)
        self._cursor.execute(sql)
        result=self._cursor.fetchall()
        self._conn.commit()
        # except:
        #     self._conn.rollback()
        return result

    def executeMany(self,query,values):
        """
        :param query: insert into table(field1,field2) values(%s,%s)
        :param values: [(field1_value1,field2_value2),(field1_value3,field2_value4)]
        :return:
        """
        # try:
        # 为了避免连接被服务器关闭,检测进行重连
        self._conn.ping(reconnect=True)
        num=len(values)
        n=0
        while n<num:
            self._cursor.executemany(query, values[n:n+1000])
            self._conn.commit()
            n+=1000
        # except:
        #     self._conn.rollback()

    def closeAll(self):
        self._cursor.close()
        self._conn.close()