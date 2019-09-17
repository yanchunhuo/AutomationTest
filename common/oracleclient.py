#-*- coding:utf-8 -*-
import cx_Oracle

class OracleClient:
    def __init__(self,host,port,username,password,dbname):
        self._dsn=cx_Oracle.makedsn(host,port,dbname)
        self._conn=cx_Oracle.connect(user=username,password=password,dsn=self._dsn)
        self._cursor=self._conn.cursor()

    def updateSQL(self, sql):
        """
        增、删操作
        :param sql:
        :return:
        """
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except Exception as e:
            print(e.args.__str__())
            self._conn.rollback()

    def querySQL(self,sql):
        result=None
        try:
            self._cursor.execute(sql)
            result=self._cursor.fetchall()
            self._conn.commit()
        except Exception as e:
            print(e.args.__str__())
            self._conn.rollback()
        return result

    def executeMany(self, query, values):
        """
        :param query: insert into table(field1,field2) values(:1,:2)
        :param values: [(field1_value1,field2_value2),(field1_value3,field2_value4)]
        :return:
        """
        try:
            self._cursor.executemany(query, values)
            self._conn.commit()
        except Exception as e:
            print(e.args.__str__())
            self._conn.rollback()

    def closeAll(self):
        self._cursor.close()
        self._conn.close()