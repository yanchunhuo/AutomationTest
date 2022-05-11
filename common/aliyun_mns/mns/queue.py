#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
from .mns_client import MNSClient
from .mns_request import *
from .mns_exception import *

class Queue:
    def __init__(self, queue_name, mns_client, debug=False): 
        self.queue_name = queue_name
        self.mns_client = mns_client
        self.set_encoding(True)
        self.debug = debug

    def set_debug(self, debug):
        self.debug = debug

    def set_encoding(self, encoding):
        """ 设置是否对消息体进行base64编码

            @type encoding: bool
            @param encoding: 是否对消息体进行base64编码
        """
        self.encoding = encoding
        
    def create(self, queue_meta, req_info=None):
        """ 创建队列

            @type queue_meta: QueueMeta object
            @param queue_meta: QueueMeta对象，设置队列的属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: string
            @return 新创建队列的URL

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = CreateQueueRequest(self.queue_name, queue_meta.visibility_timeout, queue_meta.maximum_message_size, queue_meta.message_retention_period, queue_meta.delay_seconds, queue_meta.polling_wait_seconds, queue_meta.logging_enabled)
        req.set_req_info(req_info)
        resp = CreateQueueResponse()
        self.mns_client.create_queue(req, resp)
        self.debuginfo(resp)
        return resp.queue_url

    def get_attributes(self, req_info=None):
        """ 获取队列属性

            @rtype: QueueMeta object
            @return 队列的属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = GetQueueAttributesRequest(self.queue_name)
        req.set_req_info(req_info)
        resp = GetQueueAttributesResponse()
        self.mns_client.get_queue_attributes(req, resp)
        queue_meta = QueueMeta()
        self.__resp2meta__(queue_meta, resp)
        self.debuginfo(resp)
        return queue_meta

    def set_attributes(self, queue_meta, req_info=None):
        """ 设置队列属性

            @type queue_meta: QueueMeta object
            @param queue_meta: 新设置的属性

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = SetQueueAttributesRequest(self.queue_name, queue_meta.visibility_timeout, queue_meta.maximum_message_size, queue_meta.message_retention_period, queue_meta.delay_seconds, queue_meta.polling_wait_seconds, queue_meta.logging_enabled)
        req.set_req_info(req_info)
        resp = SetQueueAttributesResponse()
        self.mns_client.set_queue_attributes(req, resp)
        self.debuginfo(resp)
    
    def delete(self, req_info=None):
        """ 删除队列

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = DeleteQueueRequest(self.queue_name)
        req.set_req_info(req_info)
        resp = DeleteQueueResponse()
        self.mns_client.delete_queue(req, resp)
        self.debuginfo(resp)

    def send_message(self, message, req_info=None):
        """ 发送消息

            @type message: Message object
            @param message: 发送的Message object

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: Message object
            @return 消息发送成功的返回属性，包含MessageId和MessageBodyMD5

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = SendMessageRequest(self.queue_name, message.message_body, message.delay_seconds, message.priority, self.encoding)
        req.set_req_info(req_info)
        resp = SendMessageResponse()
        self.mns_client.send_message(req, resp)
        self.debuginfo(resp)
        return self.__send_resp2msg__(resp)

    def batch_send_message(self, messages, req_info=None):
        """批量发送消息
           
            @type messages: list of Message object
            @param messages: 发送的Message object list

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: list of Message object
            @return 多条消息发送成功的返回属性，包含MessageId和MessageBodyMD5

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = BatchSendMessageRequest(self.queue_name, self.encoding)
        req.set_req_info(req_info)
        for msg in messages:
            req.add_message(msg.message_body, msg.delay_seconds, msg.priority)
        resp = BatchSendMessageResponse()
        self.mns_client.batch_send_message(req, resp)
        self.debuginfo(resp)
        return self.__batchsend_resp2msg__(resp)

    def peek_message(self, req_info=None):
        """ 查看消息

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: Message object
            @return: Message object中包含消息的基本属性

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = PeekMessageRequest(self.queue_name)
        req.set_req_info(req_info)
        resp = PeekMessageResponse()
        self.mns_client.peek_message(req, resp)
        self.debuginfo(resp)
        return self.__peek_resp2msg__(resp)

    def batch_peek_message(self, batch_size, req_info=None):
        """ 批量查看消息
            
            @type batch_size: int
            @param batch_size: 本次请求最多获取的消息条数

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: list of Message object
            @return 多条消息的属性，包含消息的基本属性

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = BatchPeekMessageRequest(self.queue_name, batch_size)
        req.set_req_info(req_info)
        resp = BatchPeekMessageResponse()
        self.mns_client.batch_peek_message(req, resp)
        self.debuginfo(resp)
        return self.__batchpeek_resp2msg__(resp)

    def receive_message(self, wait_seconds = -1, req_info=None):
        """ 消费消息

            @type wait_seconds: int
            @param wait_seconds: 本次请求的长轮询时间，单位：秒

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: Message object
            @return Message object中包含基本属性、下次可消费时间和临时句柄

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = ReceiveMessageRequest(self.queue_name, self.encoding, wait_seconds)
        req.set_req_info(req_info)
        resp = ReceiveMessageResponse()
        self.mns_client.receive_message(req, resp)
        self.debuginfo(resp)
        return self.__recv_resp2msg__(resp)
   
    def batch_receive_message(self, batch_size, wait_seconds = -1, req_info=None):
        """ 批量消费消息

            @type batch_size: int
            @param batch_size: 本次请求最多获取的消息条数

            @type wait_seconds: int
            @param wait_seconds: 本次请求的长轮询时间，单位：秒

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: list of Message object
            @return 多条消息的属性，包含消息的基本属性、下次可消费时间和临时句柄

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = BatchReceiveMessageRequest(self.queue_name, batch_size, self.encoding, wait_seconds)
        req.set_req_info(req_info)
        resp = BatchReceiveMessageResponse()
        self.mns_client.batch_receive_message(req, resp)
        self.debuginfo(resp)
        return self.__batchrecv_resp2msg__(resp)

    def delete_message(self, receipt_handle, req_info=None):
        """ 删除消息

            @type receipt_handle: string
            @param receipt_handle: 最近一次操作该消息返回的临时句柄

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = DeleteMessageRequest(self.queue_name, receipt_handle)
        req.set_req_info(req_info)
        resp = DeleteMessageResponse()
        self.mns_client.delete_message(req, resp)
        self.debuginfo(resp)

    def batch_delete_message(self, receipt_handle_list, req_info=None):
        """批量删除消息
            
            @type receipt_handle_list: list
            @param receipt_handle_list: batch_receive_message返回的多条消息的临时句柄

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = BatchDeleteMessageRequest(self.queue_name, receipt_handle_list)
        req.set_req_info(req_info)
        resp = BatchDeleteMessageResponse()
        self.mns_client.batch_delete_message(req, resp)
        self.debuginfo(resp)

    def change_message_visibility(self, reciept_handle, visibility_timeout, req_info=None):
        """ 修改消息下次可消费时间

            @type reciept_handle: string
            @param reciept_handle: 最近一次操作该消息返回的临时句柄

            @type visibility_timeout: int
            @param visibility_timeout: 消息下次可被消费时间为
                                       now+visibility_timeout, 单位：秒

            @type req_info: RequestInfo object
            @param req_info: 透传到MNS的请求信息

            @rtype: Message object
            @return: Message object包含临时句柄和下次可消费时间

            @note: Exception
            :: MNSClientParameterException  参数格式异常
            :: MNSClientNetworkException    网络异常
            :: MNSServerException           mns处理异常
        """
        req = ChangeMessageVisibilityRequest(self.queue_name, reciept_handle, visibility_timeout)
        req.set_req_info(req_info)
        resp = ChangeMessageVisibilityResponse()
        self.mns_client.change_message_visibility(req, resp)
        self.debuginfo(resp)
        return self.__changevis_resp2msg__(resp)

    def debuginfo(self, resp):
        if self.debug:
            print("===================DEBUG INFO===================")
            print("RequestId: %s" % resp.header["x-mns-request-id"])
            print("================================================")
    
    def __resp2meta__(self, queue_meta, resp):
        queue_meta.visibility_timeout = resp.visibility_timeout
        queue_meta.maximum_message_size = resp.maximum_message_size
        queue_meta.message_retention_period = resp.message_retention_period
        queue_meta.delay_seconds = resp.delay_seconds
        queue_meta.polling_wait_seconds = resp.polling_wait_seconds
        queue_meta.logging_enabled = resp.logging_enabled

        queue_meta.active_messages = resp.active_messages
        queue_meta.inactive_messages = resp.inactive_messages
        queue_meta.delay_messages = resp.delay_messages
        queue_meta.create_time = resp.create_time
        queue_meta.last_modify_time = resp.last_modify_time
        queue_meta.queue_name = resp.queue_name

    def __send_resp2msg__(self, resp):
        msg = Message()
        msg.message_id = resp.message_id
        msg.message_body_md5 = resp.message_body_md5
        msg.receipt_handle = resp.receipt_handle
        return msg
        
    def __batchsend_resp2msg__(self, resp):
        msg_list = []
        for entry in resp.message_list:
            msg = Message()
            msg.message_id = entry.message_id
            msg.message_body_md5 = entry.message_body_md5
            msg_list.append(msg)
        return msg_list

    def __peek_resp2msg__(self, resp):
        msg = Message()
        msg.message_id = resp.message_id
        msg.message_body_md5 = resp.message_body_md5
        msg.dequeue_count = resp.dequeue_count
        msg.enqueue_time = resp.enqueue_time
        msg.first_dequeue_time = resp.first_dequeue_time
        msg.message_body = resp.message_body
        msg.priority = resp.priority
        return msg
       
    def __batchpeek_resp2msg__(self, resp):
        msg_list = []
        for entry in resp.message_list:
            msg = Message()
            msg.message_id = entry.message_id
            msg.message_body_md5 = entry.message_body_md5
            msg.dequeue_count = entry.dequeue_count 
            msg.enqueue_time = entry.enqueue_time 
            msg.first_dequeue_time = entry.first_dequeue_time
            msg.message_body = entry.message_body
            msg.priority = entry.priority
            msg_list.append(msg)
        return msg_list            

    def __recv_resp2msg__(self, resp):
        msg = self.__peek_resp2msg__(resp)
        msg.receipt_handle = resp.receipt_handle
        msg.next_visible_time = resp.next_visible_time
        return msg

    def __batchrecv_resp2msg__(self, resp):
        msg_list = []
        for entry in resp.message_list:
            msg = Message()
            msg.message_id = entry.message_id
            msg.message_body_md5 = entry.message_body_md5
            msg.dequeue_count = entry.dequeue_count
            msg.enqueue_time = entry.enqueue_time
            msg.first_dequeue_time = entry.first_dequeue_time
            msg.message_body = entry.message_body
            msg.priority = entry.priority
            msg.next_visible_time = entry.next_visible_time
            msg.receipt_handle = entry.receipt_handle
            msg_list.append(msg)
        return msg_list            

    def __changevis_resp2msg__(self, resp):
        msg = Message()
        msg.receipt_handle = resp.receipt_handle
        msg.next_visible_time = resp.next_visible_time
        return msg

class QueueMeta:
    DEFAULT_VISIBILITY_TIMEOUT = 30
    DEFAULT_MAXIMUM_MESSAGE_SIZE = 2048
    DEFAULT_MESSAGE_RETENTION_PERIOD = 86400
    DEFAULT_DELAY_SECONDS = 0
    DEFAULT_POLLING_WAIT_SECONDS = 0
    def __init__(self, vis_timeout = None, max_msg_size = None, msg_ttl = None, delay_sec = None, polling_wait_sec = None, logging_enabled = None):
        """ 队列属性
            @note: 设置属性
            :: visibility_timeout: message被receive后，持续不可消费的时间, 单位：秒
            :: maximum_message_size: message body的最大长度, 单位：Byte
            :: message_retention_period: message最长存活时间，单位：秒
            :: delay_seconds: 新message可消费的默认延迟时间，单位：秒
            :: polling_wait_seconds: receive message时，长轮询时间，单位：秒
            :: logging_enabled: 是否开启logging功能，如果开启MNS将该队列的日志推送到Account的logging bucket中
            
            @note: 非设置属性
            :: active_messages: 可消费消息数，近似值
            :: inactive_messages: 正在被消费的消息数，近似值
            :: delay_messages: 延迟消息数，近似值
            :: create_time: queue创建时间，单位：秒 
            :: last_modify_time: 修改queue属性的最近时间，单位：秒
            :: queue_name: 队列名称
        """
        self.visibility_timeout = QueueMeta.DEFAULT_VISIBILITY_TIMEOUT if vis_timeout is None else vis_timeout
        self.maximum_message_size = QueueMeta.DEFAULT_MAXIMUM_MESSAGE_SIZE if max_msg_size is None else max_msg_size
        self.message_retention_period = QueueMeta.DEFAULT_MESSAGE_RETENTION_PERIOD if msg_ttl is None else msg_ttl
        self.delay_seconds = QueueMeta.DEFAULT_DELAY_SECONDS if delay_sec is None else delay_sec
        self.polling_wait_seconds = QueueMeta.DEFAULT_POLLING_WAIT_SECONDS if polling_wait_sec is None else polling_wait_sec
        self.logging_enabled = logging_enabled

        self.active_messages = -1
        self.inactive_messages = -1
        self.delay_messages = -1
        self.create_time = -1
        self.last_modify_time = -1
        self.queue_name = ""

    def set_visibilitytimeout(self, visibility_timeout):
        self.visibility_timeout = visibility_timeout

    def set_maximum_message_size(self, maximum_message_size):
        self.maximum_message_size = maximum_message_size
    
    def set_message_retention_period(self, message_retention_period):
        self.message_retention_period = message_retention_period

    def set_delay_seconds(self, delay_seconds):
        self.delay_seconds = delay_seconds

    def set_polling_wait_seconds(self, polling_wait_seconds):
        self.polling_wait_seconds = polling_wait_seconds

    def set_logging_enabled(self, logging_enabled):
        self.logging_enabled = logging_enabled

    def __str__(self):
        meta_info = {"VisibilityTimeout" : self.visibility_timeout,
                     "MaximumMessageSize" : self.maximum_message_size,
                     "MessageRetentionPeriod" : self.message_retention_period,
                     "DelaySeconds" : self.delay_seconds,
                     "PollingWaitSeconds" : self.polling_wait_seconds,
                     "ActiveMessages" : self.active_messages,
                     "InactiveMessages" : self.inactive_messages,
                     "DelayMessages" : self.delay_messages,
                     "CreateTime" : time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.create_time)),
                     "LastModifyTime" : time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(self.last_modify_time)),
                     "QueueName" : self.queue_name,
                     "LoggingEnabled" : self.logging_enabled}
        return "\n".join(["%s: %s"%(k.ljust(30),v) for k,v in meta_info.items()])

class Message:
    def __init__(self, message_body = None, delay_seconds = None, priority = None):
        """ 消息属性

            @note: send_message 指定属性
            :: message_body         消息体 
            :: delay_seconds        消息延迟时间
            :: priority             消息优先级

            @note: send_message 返回属性
            :: message_id           消息编号
            :: message_body_md5     消息体的MD5值

            @note: peek_message 返回属性(基本属性)
            :: message_body         消息体
            :: message_id           消息编号
            :: message_body_md5     消息体的MD5值
            :: dequeue_count        消息被消费的次数
            :: enqueue_time         消息发送到队列的时间，单位：毫秒
            :: first_dequeue_time   消息第一次被消费的时间，单位：毫秒

            @note: receive_message 返回属性，除基本属性外
            :: receipt_handle       下次删除或修改消息的临时句柄，next_visible_time之前有效
            :: next_visible_time    消息下次可消费时间

            @note: change_message_visibility 返回属性
            :: receipt_handle
            :: next_visible_time
        """
        self.message_body = "" if message_body is None else message_body
        self.delay_seconds = -1 if delay_seconds is None else delay_seconds
        self.priority = -1 if priority is None else priority

        self.message_id = ""
        self.message_body_md5 = ""

        self.dequeue_count = -1
        self.enqueue_time = -1
        self.first_dequeue_time = -1

        self.receipt_handle = ""
        self.next_visible_time = 1

    def set_delayseconds(self, delay_seconds):
        self.delay_seconds = delay_seconds

    def set_priority(self, priority):
        self.priority = priority

