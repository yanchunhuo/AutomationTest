#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class RequestBase:
    def __init__(self):
        self.method = ""
        self.request_id = None

    def set_req_info(self, req_info):
        if req_info is not None:
            if req_info.request_id is not None:
                self.request_id = req_info.request_id

class ResponseBase():
    def __init__(self):
        self.status = -1
        self.header = {}
        self.error_data = ""

    def get_requestid(self):
        return self.header.get("x-mns-request-id")

class SetAccountAttributesRequest(RequestBase):
    def __init__(self, logging_bucket = None):
        RequestBase.__init__(self)
        self.logging_bucket = logging_bucket
        self.method = "PUT"

class SetAccountAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class GetAccountAttributesRequest(RequestBase):
    def __init__(self):
        RequestBase.__init__(self)
        self.method = "GET"

class GetAccountAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.logging_bucket = ""

class CreateQueueRequest(RequestBase):
    def __init__(self, queue_name, visibility_timeout = -1, maximum_message_size = -1, message_retention_period = -1, delay_seconds = -1, polling_wait_seconds = -1, logging_enabled = None):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.visibility_timeout = visibility_timeout
        self.maximum_message_size = maximum_message_size
        self.message_retention_period = message_retention_period
        self.delay_seconds = delay_seconds
        self.polling_wait_seconds = polling_wait_seconds
        self.logging_enabled = logging_enabled
        self.method = "PUT"

class CreateQueueResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.queue_url = ""

class DeleteQueueRequest(RequestBase):
    def __init__(self, queue_name):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.method = "DELETE"

class DeleteQueueResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class ListQueueRequest(RequestBase):
    def __init__(self, prefix = u"", ret_number = -1, marker = u"", with_meta = False):
        RequestBase.__init__(self)
        self.prefix = prefix
        self.ret_number = ret_number
        self.marker = marker
        self.with_meta = with_meta
        self.method = "GET"

class ListQueueResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.queueurl_list = []
        self.next_marker = u""
        self.queuemeta_list = []

class SetQueueAttributesRequest(RequestBase):
    def __init__(self, queue_name, visibility_timeout = -1, maximum_message_size = -1, message_retention_period = -1, delay_seconds = -1, polling_wait_seconds = -1, logging_enabled = None):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.visibility_timeout = visibility_timeout
        self.maximum_message_size = maximum_message_size
        self.message_retention_period = message_retention_period
        self.delay_seconds = delay_seconds
        self.polling_wait_seconds = polling_wait_seconds
        self.logging_enabled = logging_enabled
        self.method = "PUT"

class SetQueueAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class GetQueueAttributesRequest(RequestBase):
    def __init__(self, queue_name):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.method = "GET"

class GetQueueAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.active_messages = -1
        self.create_time = -1
        self.delay_messages = -1
        self.delay_seconds = -1
        self.inactive_messages = -1
        self.last_modify_time = -1
        self.maximum_message_size = -1
        self.message_retention_period = -1
        self.queue_name = ""
        self.visibility_timeout = -1
        self.polling_wait_seconds = -1
        self.logging_enable = None

class SendMessageRequest(RequestBase):
    def __init__(self, queue_name, message_body, delay_seconds = -1, priority = -1, base64encode = True):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.message_body = message_body
        self.delay_seconds = delay_seconds
        self.priority = priority
        self.base64encode = base64encode
        self.method = "POST"

class SendMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_id = ""
        self.message_body_md5 = ""
        self.receipt_handle = ""

class SendMessageRequestEntry:
    def __init__(self, message_body, delay_seconds = -1, priority = -1):
        self.message_body = message_body
        self.delay_seconds = delay_seconds
        self.priority = priority

class BatchSendMessageRequest(RequestBase):
    def __init__(self, queue_name, base64encode):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.base64encode = base64encode
        self.method = "POST"
        self.message_list = []

    def add_message(self, message_body, delay_seconds = -1, priority = -1):
        msg = SendMessageRequestEntry(message_body, delay_seconds, priority)
        self.message_list.append(msg)

class SendMessageResponseEntry:
    def __init__(self):
        self.message_id = ""
        self.message_body_md5 = ""

class BatchSendMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_list = []

class PeekMessageRequest(RequestBase):
    def __init__(self, queue_name, base64decode = True):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.base64decode = base64decode
        self.method = "GET"

class PeekMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.dequeue_count = -1
        self.enqueue_time = -1
        self.first_dequeue_time = -1
        self.message_body = ""
        self.message_id = ""
        self.message_body_md5 = ""
        self.priority = -1

class BatchPeekMessageRequest(RequestBase):
    def __init__(self, queue_name, batch_size, base64decode = True):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.batch_size = batch_size
        self.base64decode = base64decode
        self.method = "GET"

class PeekMessageResponseEntry:
    def __init__(self):
        self.dequeue_count = -1
        self.enqueue_time = -1
        self.first_dequeue_time = -1
        self.message_body = ""
        self.message_id = ""
        self.message_body_md5 = ""
        self.priority = -1

class BatchPeekMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_list = []

class ReceiveMessageRequest(RequestBase):
    def __init__(self, queue_name, base64decode = True, wait_seconds = -1):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.base64decode = base64decode
        self.wait_seconds = wait_seconds
        self.method = "GET"

class ReceiveMessageResponse(PeekMessageResponse):
    def __init__(self):
        PeekMessageResponse.__init__(self)
        self.next_visible_time = -1
        self.receipt_handle = ""

class BatchReceiveMessageRequest(RequestBase):
    def __init__(self, queue_name, batch_size, base64decode = True, wait_seconds = -1):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.batch_size = batch_size
        self.base64decode = base64decode
        self.wait_seconds = wait_seconds
        self.method = "GET"

class ReceiveMessageResponseEntry():
    def __init__(self):
        self.dequeue_count = -1
        self.enqueue_time = -1
        self.first_dequeue_time = -1
        self.message_body = ""
        self.message_id = ""
        self.message_body_md5 = ""
        self.priority = -1
        self.next_visible_time = ""
        self.receipt_handle = ""

class BatchReceiveMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_list = []

class DeleteMessageRequest(RequestBase):
    def __init__(self, queue_name, receipt_handle):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.receipt_handle = receipt_handle
        self.method = "DELETE"

class DeleteMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class BatchDeleteMessageRequest(RequestBase):
    def __init__(self, queue_name, receipt_handle_list):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.receipt_handle_list = receipt_handle_list
        self.method = "DELETE"

class BatchDeleteMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class ChangeMessageVisibilityRequest(RequestBase):
    def __init__(self, queue_name, receipt_handle, visibility_timeout):
        RequestBase.__init__(self)
        self.queue_name = queue_name
        self.receipt_handle = receipt_handle
        self.visibility_timeout = visibility_timeout
        self.method = "PUT"

class ChangeMessageVisibilityResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.receipt_handle = ""
        self.next_visible_time = -1

class CreateTopicRequest(RequestBase):
    def __init__(self, topic_name, maximum_message_size = -1, logging_enabled = None):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.maximum_message_size = maximum_message_size
        self.logging_enabled = logging_enabled
        self.method = "PUT"

class CreateTopicResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.topic_url = ""

class DeleteTopicRequest(RequestBase):
    def __init__(self, topic_name):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.method = "DELETE"

class DeleteTopicResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class ListTopicRequest(RequestBase):
    def __init__(self, prefix = "", ret_number = -1, marker = "", with_meta = False):
        RequestBase.__init__(self)
        self.prefix = prefix
        self.ret_number = ret_number
        self.marker = marker
        self.with_meta = with_meta
        self.method = "GET"

class ListTopicResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.topicurl_list = []
        self.next_marker = ""
        self.topicmeta_list = []

class SetTopicAttributesRequest(RequestBase):
    def __init__(self, topic_name, maximum_message_size = -1, logging_enabled = None):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.maximum_message_size = maximum_message_size
        self.logging_enabled = logging_enabled
        self.method = "PUT"

class SetTopicAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class GetTopicAttributesRequest(RequestBase):
    def __init__(self, topic_name):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.method = "GET"

class GetTopicAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_count = -1
        self.create_time = -1
        self.last_modify_time = -1
        self.maximum_message_size = -1
        self.message_retention_period = -1
        self.topic_name = ""
        self.logging_enabled = None

class PublishMessageRequest(RequestBase):
    def __init__(self, topic_name, message_body, message_tag="", direct_mail=None, direct_sms=None):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.message_body = message_body
        self.message_tag = message_tag
        self.direct_mail = direct_mail
        self.direct_sms = direct_sms
        self.method = "POST"

class PublishMessageResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.message_id = ""
        self.message_body_md5 = ""

class SubscribeRequest(RequestBase):
    def __init__(self, topic_name, subscription_name, endpoint, notify_strategy = "", notify_content_format = "", filter_tag = ""):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.endpoint = endpoint
        self.filter_tag = filter_tag
        self.notify_strategy = notify_strategy
        self.notify_content_format = notify_content_format
        self.method = "PUT"

class SubscribeResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.subscription_url = ""

class UnsubscribeRequest(RequestBase):
    def __init__(self, topic_name, subscription_name):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.method = "DELETE"

class UnsubscribeResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class ListSubscriptionByTopicRequest(RequestBase):
    def __init__(self, topic_name, prefix = "", ret_number = -1, marker = ""):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.prefix = prefix
        self.ret_number = ret_number
        self.marker = marker
        self.method = "GET"

class ListSubscriptionByTopicResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.subscriptionurl_list = []
        self.next_marker = ""
        self.subscriptionmeta_list = []

class SetSubscriptionAttributesRequest(RequestBase):
    def __init__(self, topic_name, subscription_name, endpoint = "", notify_strategy = "", notify_content_format = "", filter_tag = ""):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.endpoint = endpoint
        self.filter_tag = filter_tag
        self.notify_strategy = notify_strategy
        self.notify_content_format = notify_content_format
        self.method = "PUT"

class SetSubscriptionAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)

class GetSubscriptionAttributesRequest(RequestBase):
    def __init__(self, topic_name, subscription_name):
        RequestBase.__init__(self)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.method = "GET"

class GetSubscriptionAttributesResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.topic_owner = ""
        self.topic_name = ""
        self.subscription_name = ""
        self.endpoint = ""
        self.filter_tag = ""
        self.notify_strategy = ""
        self.notify_content_format = ""
        self.create_time = -1
        self.last_modify_time = -1

class OpenServiceRequest(RequestBase):
    def __init__(self):
        RequestBase.__init__(self)
        self.method = "POST"


class OpenServiceResponse(ResponseBase):
    def __init__(self):
        ResponseBase.__init__(self)
        self.oder_id = ""