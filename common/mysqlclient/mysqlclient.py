#-*- coding:utf-8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import pymysql

class MysqlClient:
    def __init__(self,host,port,username,password,dbname,charset='utf8',cursorclass=pymysql.cursors.DictCursor):
        self.conn=pymysql.connect(host=host,port=int(port),user=username,password=password,db=dbname,charset=charset,
                                  cursorclass=cursorclass)

    def executeSQL(self,sql):
        # try:
        # 为了避免连接被服务器关闭,检测进行重连
        self.conn.ping(reconnect=True)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            result=cursor.fetchall()
        self.conn.commit()
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
        self.conn.ping(reconnect=True)
        num=len(values)
        n=0
        with self.conn.cursor() as cursor:
            while n<num:
                cursor.executemany(query, values[n:n+1000])
                self.conn.commit()
                n+=1000
        # except:
        #     self._conn.rollback()

    def closeAll(self):
        self.conn.close()