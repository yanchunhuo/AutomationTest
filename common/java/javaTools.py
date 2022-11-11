#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
import os
import jpype

class JavaTool:

    @classmethod
    def getAllJar(cls):
        result=[]
        libpath=os.path.join(os.path.abspath('common/java/lib/'),'')
        path=os.walk(libpath)
        for dirpath,dirname,filenames in path:
            for filename in filenames:
                if filename.endswith('.jar'):
                    filepath=os.path.join(dirpath,filename)
                    result.append(filepath)
        return result

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
            jpype.startJVM(jpype.getClassPath(),classpath=JavaTool.getAllJar(),convertStrings=False)

            self.__inited = True