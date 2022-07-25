#
# sqlacodegen_sqlite_tool.py
# @author yanchunhuo
# @description 
# @created 2022-07-25T19:23:33.845Z+08:00
# @last-modified 2022-07-25T19:57:36.776Z+08:00
# github https://github.com/yanchunhuo

import platform
import subprocess

class Sqlacodegen_Sqlite_Tool:
    def __init__(self,file_path) -> None:
        """_summary_

        Args:
            file_path (_type_): _description_
        """
        self.url='sqlite:///%s'%(file_path)
        
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