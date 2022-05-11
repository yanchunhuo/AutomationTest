#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .mns_client import MNSClient
from .mns_request import *
from .queue import Queue
from .topic import Topic
from .subscription import Subscription
from .mns_tool import MNSLogger

class Account:
    def __init__(self, host, access_id, access_key, security_token = "", debug=False, logger = None):
        """
            @type host: string
            @param host: 访问的url，例如：http://$accountid.mns.cn-hangzhou.aliyuncs.com

            @type access_id: string
            @param access_id: 用户的AccessId, 阿里云官网获取

            @type access_key: string
            @param access_key: 用户的AccessKey，阿里云官网获取

            @type security_token: string
            @param security_token: 如果用户使用STS Token访问，需要提供security_token

            @note: Exception
            :: MNSClientParameterException host格式错误
        """
        self.access_id = access_id
        self.access_key = access_key
        self.security_token = security_token
        self.debug = debug
        self.logger = logger
        self.mns_client = MNSClient(host, access_id, access_key, security_token = security_token, logger=self.logger)

    def set_debug(self, debug):
        self.debug = debug

    def set_log_level(self, log_level):
        """ 设置logger的日志级别
            @type log_level: int
            @param log_level: one of logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL
        """
        MNSLogger.validate_loglevel(log_level)
        self.logger.setLevel(log_level)
        self.mns_client.set_log_level(log_level)

    def close_log(self):
        """ 关闭日志打印
        """
        self.mns_client.close_log()

    def set_client(self, host, access_id=None, access_key=None, security_token=None):
        """ 设置访问的url

            @type host: string
            @param host: 访问的url，例如：http://$accountid-new.mns.cn-hangzhou.aliyuncs.com

            @type access_id: string
            @param access_id: 用户的AccessId，阿里云官网获取

            @type access_key: string
            @param access_key: 用户的AccessKey，阿里云官网获取

            @type security_token: string
            @param security_token: 用户使用STS Token访问，需要提供security_token；如果不再使用 STS Token，请设置为 ""

            @note: Exception
            :: MNSClientParameterException host格式错误
        """
        if access_id is None:
            access_id = self.access_id
        if access_key is None:
            access_key = self.access_key
        if security_token is None:
            security_token = self.security_token
        self.mns_client = MNSClient(host, access_id, access_key, security_token=security_token, logger=self.logger)

    def set_attributes(self, account_meta, req_info=None):
        """ 设置Account的属性

            @type account_meta: AccountMeta object
            @param queue_meta: 新设置的属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = SetAccountAttributesRequest(account_meta.logging_bucket)
        req.set_req_info(req_info)
        resp = SetAccountAttributesResponse()
        self.mns_client.set_account_attributes(req, resp)
        self.debuginfo(resp)

    def get_attributes(self, req_info=None):
        """ 获取Account的属性

            @rtype: AccountMeta object
            @return: 返回该Account的Meta属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = GetAccountAttributesRequest()
        req.set_req_info(req_info)
        resp = GetAccountAttributesResponse()
        self.mns_client.get_account_attributes(req, resp)
        account_meta = AccountMeta()
        self.__resp2meta__(account_meta, resp)
        self.debuginfo(resp)
        return account_meta

    def get_queue(self, queue_name):
        """ 获取Account的一个Queue对象

            @type queue_name: string
            @param queue_name: 队列名

            @rtype: Queue object
            @return: 返回该Account的一个Queue对象
        """
        return Queue(queue_name, self.mns_client, self.debug)

    def get_topic(self, topic_name):
        """ 获取Account的一个Topic对象

            @type topic_name: string
            @param topic_name: 主题名称

            @rtype: Topic object
            @return: 返回该Account的一个Topic对象
        """
        return Topic(topic_name, self.mns_client, self.debug)

    def get_subscription(self, topic_name, subscription_name):
        """ 获取Account的一个Subscription对象

            @type topic_name: string
            @param topic_name: 主题名称

            @type subscription_name: string
            @param subscription_name: 订阅名称

            @rtype: Subscription object
            @return: 返回该Account指定Topic的一个Subscription对象
        """
        return Subscription(topic_name, subscription_name, self.mns_client, self.debug)

    def get_client(self):
        """ 获取queue client

            @rtype: MNSClient object
            @return: 返回使用的MNSClient object
        """
        return self.mns_client

    def list_queue(self, prefix = "", ret_number = -1, marker = "", req_info=None):
        """ 列出Account的队列

            @type prefix: string
            @param prefix: 队列名的前缀

            @type ret_number: int
            @param ret_number: list_queue最多返回的队列数

            @type marker: string
            @param marker: list_queue的起始位置，上次list_queue返回的next_marker

            @rtype: tuple
            @return: QueueURL的列表和下次list queue的起始位置; 如果所有queue都list出来，next_marker为"".

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = ListQueueRequest(prefix, ret_number, marker)
        req.set_req_info(req_info)
        resp = ListQueueResponse()
        self.mns_client.list_queue(req, resp)
        self.debuginfo(resp)
        return resp.queueurl_list, resp.next_marker

    def list_topic(self, prefix = "", ret_number = -1, marker = "", req_info=None):
        """ 列出Account的主题

            @type prefix: string
            @param prefix: 主题名称的前缀

            @type ret_number: int
            @param ret_number: list_topic最多返回的主题个数

            @type marker: string
            @param marker: list_topic的起始位置，上次list_topic返回的next_marker

            @rtype: tuple
            @return: TopicURL的列表,下次list topic的起始位置, 如果所有主题都返回时，next_marker为""

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = ListTopicRequest(prefix, ret_number, marker, True)
        req.set_req_info(req_info)
        resp = ListTopicResponse()
        self.mns_client.list_topic(req, resp)
        self.debuginfo(resp)
        return resp.topicurl_list, resp.next_marker

    def open_service(self, req_info=None):
        req = OpenServiceRequest()
        req.set_req_info(req_info)
        resp = OpenServiceResponse()
        self.mns_client.open_service(req, resp)
        return resp

    def debuginfo(self, resp):
        if self.debug:
            print("===================DEBUG INFO===================")
            print("RequestId: %s" % resp.header["x-mns-request-id"])
            print("================================================")

    def __resp2meta__(self, account_meta, resp):
        account_meta.logging_bucket = resp.logging_bucket

class AccountMeta:
    def __init__(self, logging_bucket = None):
        """ Account属性
            @note: 可设置属性
            :: logging_bucket: 保存用户操作MNS日志的bucket name
        """
        self.logging_bucket = logging_bucket

    def __str__(self):
        meta_info = {"LoggingBucket" : self.logging_bucket}
        return "\n".join(["%s: %s" % (k.ljust(30),v) for k,v in meta_info.items()])
