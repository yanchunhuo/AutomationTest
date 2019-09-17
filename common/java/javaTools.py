#-*- coding:utf8 -*-
import os
import platform
import jpype

class JavaTool:

    @classmethod
    def getAllJar(cls):
        split_flag=':'
        if 'Windows'==platform.system():
            split_flag=';'
        result=''
        libpath=os.path.join(os.path.abspath('common/java/lib/'),'')
        path=os.walk(libpath)
        for dirpath,dirname,filenames in path:
            for filename in filenames:
                if filename.endswith('.jar'):
                    filepath=os.path.join(dirpath,filename)
                    result=result+split_flag+filepath
        return result.lstrip(split_flag)

class StartJpypeJVM(object):
    """
    采用单例模式，保证一个进程里只启动一个jvm
    """
    __instance = None
    __inited = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if self.__inited is None:
            jpype.startJVM(jpype.get_default_jvm_path(), "-ea", "-Djava.class.path=" + JavaTool.getAllJar())
            self.__inited = True