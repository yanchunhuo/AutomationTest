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
        :param params 格式:
                      无参数填写[]
                      基本数据类型参数：[{"type":"java.lang.String","data":"value"}]
                      数组、集合类型参数：[{"type":"java.util.Set","data":[{"type":"java.lang.Long","data":"value"},{"type":"java.lang.Long","data":"value"}]}]
                      MAP类型参数：[{"type":"java.util.Map","data":[[{"type":"key_type","data":"key_value"},{"type":"value_type","data":"value_value"}]]"}]
                      自定义对象类型参数：[{"type":"com.company.xxxDTO","data":{"username":"username","age":344}}]
                      注：type当前支持：java.lang.*、java.util.List、java.util.Set、java.util.Collection、java.util.Map
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
