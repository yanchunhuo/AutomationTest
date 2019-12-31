#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from common.java.javaTools import StartJpypeJVM
import jpype
import ujson

class DubboClient:

    def __init__(self,registryAddresses,protocol='dubbo',group=None):
        """
        :param registryAddresses 注册中心地址，多个使用逗号隔开
        :param protocol 使用协议
        :param group 组
        :return
        """
        # 启动jvm......'
        StartJpypeJVM()
        self._DubboClient=jpype.JClass("com.tools.DubboClient")
        self._dubboClient=self._DubboClient(registryAddresses,protocol,group)

    def request(self,requestInterfaceClassName,requestMethod,params):
        """
        :param requestInterfaceClassName 请求接口类名,需完整包路径
        :param requestMethod 请求方法
        :param params 无参数填写null,有参数格式:requestType##requestParamClassName##param||requestType##requestParamClassName##param
                      requestType:1:字典类型、2:数组类型、3:基础数据类型
        :return
        """
        result=self._dubboClient.request(requestInterfaceClassName,requestMethod,params)
        if result:
            return ujson.loads(result)

    def object2Json(self,className):
        """
        将对象转换成json字符串
        :param className: 需要转换的类名，需填写完整路径
        :return:
        """
        return self._DubboClient.object2Json(className)
