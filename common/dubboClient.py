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
        self. _DubboClient=jpype.JClass("com.yanchunhuo.tools.DubboClient")
        self._dubboClient=self._DubboClient(registryAddresses,protocol,group)

    def request(self,requestInterfaceClassName,requestMethod,params):
        """
        :param requestInterfaceClassName 请求接口类名,需完整包路径
        :param requestMethod 请求方法
        :param params 所有参数放在一个数组内，格式:
                      无参数填写：[]
                      参数值为null：填写null字符串即可，当前支持String、自定义对象类型
                      一个基本数据类型参数(byte、short、int、long、double、float、boolean)：[{"type":"int","data":"value"}]
                      一个基本数据类型数组参数：[{"type":"int[]","data":[{"type":"int","data":"value"},{"type":"int","data":"value"}]}]
                      一个java.lang数据类型参数：[{"type":"java.lang.String","data":"1"}]
                      一个java.lang数据类型数组参数：[{"type":"java.lang.String[]","data":[{"type":"java.lang.String","data":"value"},{"type":"java.lang.String","data":"value"}]}]
                      一个集合类型参数：[{"type":"java.util.Set","data":[{"type":"java.lang.Long","data":"value"},{"type":"java.lang.Long","data":"value"}]}]
                      一个MAP类型参数：[{"type":"java.util.Map","data":[[{"type":"key_type","data":"key_value"},{"type":"value_type","data":"value_value"}]]"}]
                      一个枚举类类型：[{"type":"com.ztjy.authority.constants.SystemTypeEnum","data":"value"}]  其中value填写枚举类中的一个枚举值
                      一个时间类型：[{"type":"java.util.Date","data":{"format":"yyyy-MM-dd HH:mm:ss","datetime":"value"}}]
                                  当前支持java.util.Date、java.time.LocalDate、java.sql.Timestamp、java.sql.Date
                      一个自定义对象类型参数：[{"type":"com.company.xxxDTO","data":{"username":"username","age":344}}]
        :return
        """
        if not isinstance(params,str):
            params=ujson.dumps(params)
        result=self._dubboClient.request(requestInterfaceClassName,requestMethod,params)
        if result:
            return ujson.loads(str(result))

    def object2Json(self,className):
        """
        将对象转换成json字符串
        :param className: 需要转换的类名，需填写完整路径
        :return:
        """
        return str(self._DubboClient.object2Json(className))