#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
from .mns_client import MNSClient
from .mns_request import *
from .mns_exception import *

class Subscription:
    def __init__(self, topic_name, subscription_name, mns_client, debug=False):
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.mns_client = mns_client
        self.debug = debug

    def set_debug(self, debug):
        self.debug = debug

    def subscribe(self, subscription_meta, req_info=None):
        """ 创建订阅

            @type subscription_meta: SubscriptionMeta object
            @param subscription_meta: SubscriptionMeta对象，指定订阅的属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: string
            @return 新创建订阅的URL

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = SubscribeRequest(self.topic_name,
                               self.subscription_name,
                               subscription_meta.endpoint,
                               subscription_meta.notify_strategy,
                               subscription_meta.notify_content_format,
                               subscription_meta.filter_tag)
        req.set_req_info(req_info)
        resp = SubscribeResponse()
        self.mns_client.subscribe(req, resp)
        self.debuginfo(resp)
        return resp.subscription_url

    def get_attributes(self, req_info=None):
        """ 获取订阅属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: SubscriptionMeta object
            @return 订阅的属性

            @note: Exception
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = GetSubscriptionAttributesRequest(self.topic_name, self.subscription_name)
        req.set_req_info(req_info)
        resp = GetSubscriptionAttributesResponse()
        self.mns_client.get_subscription_attributes(req, resp)
        subscription_meta = SubscriptionMeta()
        self.__resp2meta__(subscription_meta, resp)
        self.debuginfo(resp)
        return subscription_meta

    def set_attributes(self, subscription_meta, req_info=None):
        """ 设置订阅的属性

            @type subscription_meta: SubscriptionMeta object
            @param subscription_meta: 新设置的订阅属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = SetSubscriptionAttributesRequest(self.topic_name,
                                               self.subscription_name,
                                               subscription_meta.endpoint,
                                               subscription_meta.notify_strategy)
        req.set_req_info(req_info)
        resp = SetSubscriptionAttributesResponse()
        self.mns_client.set_subscription_attributes(req, resp)
        self.debuginfo(resp)

    def unsubscribe(self, req_info=None):
        """ 删除订阅

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = UnsubscribeRequest(self.topic_name, self.subscription_name)
        req.set_req_info(req_info)
        resp = UnsubscribeResponse()
        self.mns_client.unsubscribe(req, resp)
        self.debuginfo(resp)

    def debuginfo(self, resp):
        if self.debug:
            print("===================DEBUG INFO===================")
            print("RequestId: %s" % resp.header["x-mns-request-id"])
            print("================================================")

    def __resp2meta__(self, subscription_meta, resp):
        subscription_meta.topic_owner = resp.topic_owner
        subscription_meta.topic_name = resp.topic_name
        subscription_meta.subscription_name = resp.subscription_name
        subscription_meta.endpoint = resp.endpoint
        subscription_meta.filter_tag = resp.filter_tag
        subscription_meta.notify_strategy = resp.notify_strategy
        subscription_meta.notify_content_format = resp.notify_content_format
        subscription_meta.create_time = resp.create_time
        subscription_meta.last_modify_time = resp.last_modify_time

class SubscriptionMeta:
    def __init__(self, endpoint = "", notify_strategy = "", notify_content_format = "", filter_tag = ""):
        """ Subscription属性
            @note: 设置属性
            :: endpoint: 接收端地址, HttpEndpoint, MailEndpoint or QueueEndpoint
            :: filter_tag: 消息过滤使用的标签
            :: notify_strategy: 向Endpoint推送消息错误时的重试策略
            :: notify_content_format: 向Endpoint推送的消息内容格式

            @note: 不可设置属性
            :: topic_owner: Subscription订阅的Topic的Owner
            :: topic_name: Subscription订阅的Topic名称
            :: subscription_name: 订阅名称
            :: create_time: Subscription的创建时间，从1970-1-1 00:00:00 000到现在的秒值
            :: last_modify_time: 修改Subscription属性信息最近时间，从1970-1-1 00:00:00 000到现在的秒值
        """
        self.endpoint = endpoint
        self.filter_tag = filter_tag
        self.notify_strategy = notify_strategy
        self.notify_content_format = notify_content_format

        self.topic_owner = ""
        self.topic_name = ""
        self.subscription_name = ""
        self.create_time = -1
        self.last_modify_time = -1

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def set_filter_tag(self, filter_tag):
        self.filter_tag = filter_tag

    def set_notify_strategy(self, notify_strategy):
        self.notify_strategy = notify_strategy

    def set_notify_content_format(self, notify_content_format):
        self.notify_content_format = notify_content_format

    def __str__(self):
        meta_info = {"TopicOwner": self.topic_owner,
                     "TopicName": self.topic_name,
                     "SubscriptionName": self.subscription_name,
                     "Endpoint": self.endpoint,
                     "FilterTag": self.filter_tag,
                     "NotifyStrategy": self.notify_strategy,
                     "NotifyContentFormat": self.notify_content_format,
                     "CreateTime": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.create_time)),
                     "LastModifyTime": time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.last_modify_time))}
        return "\n".join(["%s: %s" % (k.ljust(30),v) for k,v in meta_info.items()])

class SubscriptionNotifyStrategy:
    BACKOFF = "BACKOFF_RETRY"
    EXPONENTIAL = "EXPONENTIAL_DECAY_RETRY"

class SubscriptionNotifyContentFormat:
    XML = "XML"
    SIMPLIFIED = "SIMPLIFIED"
    JSON = "JSON"
