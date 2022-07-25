#
# sqlacodegen_too.py
# @author yanchunhuo
# @description 
# @created 2022-07-21T17:00:26.678Z+08:00
# @last-modified 2022-07-25T19:57:33.428Z+08:00
# github https://github.com/yanchunhuo
import platform
import subprocess

class Sqlacodegen_Mysql_Tool:
    def __init__(self,host:str=None,port:str=None,username:str=None,password:str=None,db:str=None,driver_type='pymysql') -> None:
        """_summary_

        Args:
            host (str, optional): _description_. Defaults to None.
            port (str, optional): _description_. Defaults to None.
            username (str, optional): _description_. Defaults to None.
            password (str, optional): _description_. Defaults to None.
            db (str, optional): _description_. Defaults to None.
            driver_type (str, optional): pymysql：pymysql，mysqldb：mysqlclient. Defaults to 'pymysql'.
        """
        self.url='mysql+%s://%s:%s@%s:%s/%s'%(driver_type,username,password,host,str(port),db)
        
    def generate_table_model(self,table_name:str,output_file_path:str):
        command='sqlacodegen %s --tables %s --outfile %s'%(self.url,table_name,output_file_path)
        output = subprocess.check_output(command, shell=True, timeout=3600)
        if 'Windows' == platform.system():
            output=output.decode('cp936')
        else:
            output=output.decode('utf-8')
        return output
        
    def generate_db_models(self,output_file_path:str):
        command='sqlacodegen %s --outfile %s'%(self.url,output_file_path)
        output = subprocess.check_output(command, shell=True, timeout=3600)
        if 'Windows' == platform.system():
            output=output.decode('cp936')
        else:
            output=output.decode('utf-8')
        return output