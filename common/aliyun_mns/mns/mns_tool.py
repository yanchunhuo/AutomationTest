#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import string
import types
import logging
import logging.handlers
from .mns_exception import *

METHODS = ["PUT", "POST", "GET", "DELETE"]
PERMISSION_ACTIONS = ["setqueueattributes", "getqueueattributes", "sendmessage", "receivemessage", "deletemessage", "peekmessage", "changevisibility"]

class MNSLogger:
    @staticmethod
    def get_logger(log_name=None, log_file=None, log_level=logging.INFO):
        if log_name is None:
            log_name = "mns_python_sdk"
        if log_file is None:
            log_file = os.path.join(os.path.split(os.path.realpath(__file__))[0], "mns_python_sdk.log")
        logger = logging.getLogger(log_name)
        if logger.handlers == []:
            fileHandler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024)
            formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(thread)d] %(message)s', '%Y-%m-%d %H:%M:%S')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        MNSLogger.validate_loglevel(log_level)
        logger.setLevel(log_level)
        return logger

    @staticmethod
    def validate_loglevel(log_level):
        log_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        if log_level not in log_levels:
            raise MNSClientParameterException("LogLevelInvalid", "Bad value: '%s', expect levels: '%s'." % \
                (log_level, ','.join([str(item) for item in log_levels])))

class ValidatorBase:
    @staticmethod
    def validate(req):
        pass

    @staticmethod
    def type_validate(item, valid_type, param_name=None, req_id=None):
        if not (type(item) is valid_type):
            if param_name is None:
                raise MNSClientParameterException("TypeInvalid", "Bad type: '%s', '%s' expect type '%s'." % (type(item), item, valid_type), req_id)
            else:
                raise MNSClientParameterException("TypeInvalid", "Param '%s' in bad type: '%s', '%s' expect type '%s'." % (param_name, type(item), item, valid_type), req_id)

    @staticmethod
    def is_str(item, param_name=None, req_id=None):
        #if not isinstance(item, unicode):
        #    if param_name is None:
        #        raise MNSClientParameterException("TypeInvalid", "Bad type: '%s', '%s' expect basestring." % (type(item), item), req_id)
        #    else:
        #        raise MNSClientParameterException("TypeInvalid", "Param '%s' in bad type: '%s', '%s' expect basestring." % (param_name, type(item), item), req_id)
        return

    @staticmethod
    def marker_validate(req):
        ValidatorBase.is_str(req.marker, req_id=req.request_id)

    @staticmethod
    def retnumber_validate(req):
        #ValidatorBase.type_validate(req.ret_number, types.IntType, req_id=req.request_id)
        ValidatorBase.type_validate(req.ret_number, int, req_id=req.request_id)
        if (req.ret_number != -1 and req.ret_number <= 0 ):
            raise MNSClientParameterException("HeaderInvalid", "Bad value: '%s', x-mns-number should larger than 0." % req.ret_number, req.request_id)

    @staticmethod
    def name_validate(name, nameType, req_id=None):
        #type
        ValidatorBase.is_str(name, req_id=req_id)

        #length
        if len(name) < 1:
            raise MNSClientParameterException("QueueNameInvalid", "Bad value: '%s', the length of %s should larger than 1." % (name, nameType), req_id)

    @staticmethod
    def list_condition_validate(req):
        if req.prefix != "":
            ValidatorBase.name_validate(req.prefix, "prefix")

        ValidatorBase.marker_validate(req)
        ValidatorBase.retnumber_validate(req)

class SetAccountAttributesValidator(ValidatorBase):
    @staticmethod
    def validate(req):
        #type
        if req.logging_bucket is not None:
            ValidatorBase.is_str(req.logging_bucket, req_id=req.request_id)

class QueueValidator(ValidatorBase):
    @staticmethod
    def queue_validate(req):
        #type
        #ValidatorBase.type_validate(req.visibility_timeout, types.IntType, req_id=req.request_id)
        #ValidatorBase.type_validate(req.maximum_message_size, types.IntType, req_id=req.request_id)
        #ValidatorBase.type_validate(req.message_retention_period, types.IntType, req_id=req.request_id)
        #ValidatorBase.type_validate(req.delay_seconds, types.IntType, req_id=req.request_id)
        #ValidatorBase.type_validate(req.polling_wait_seconds, types.IntType, req_id=req.request_id)
        ValidatorBase.type_validate(req.visibility_timeout, int, req_id=req.request_id)
        ValidatorBase.type_validate(req.maximum_message_size, int, req_id=req.request_id)
        ValidatorBase.type_validate(req.message_retention_period, int, req_id=req.request_id)
        ValidatorBase.type_validate(req.delay_seconds, int, req_id=req.request_id)
        ValidatorBase.type_validate(req.polling_wait_seconds, int, req_id=req.request_id)

        #value
        if req.visibility_timeout != -1 and req.visibility_timeout <= 0:
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%d', visibility timeout should larger than 0." % req.visibility_timeout, req.request_id)
        if req.maximum_message_size != -1 and req.maximum_message_size <= 0:
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%d', maximum message size should larger than 0." % req.maximum_message_size, req.request_id)
        if req.message_retention_period != -1 and req.message_retention_period <= 0:
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%d', message retention period should larger than 0." % req.message_retention_period, req.request_id)
        if req.delay_seconds != -1 and req.delay_seconds < 0:
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%d', delay seconds should larger than 0." % req.delay_seconds, req.request_id)
        if req.polling_wait_seconds != -1 and req.polling_wait_seconds < 0:
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%d', polling wait seconds should larger than 0." % req.polling_wait_seconds, req.request_id)
        if req.logging_enabled != None and str(req.logging_enabled).lower() not in ("true", "false"):
            raise MNSClientParameterException("QueueAttrInvalid", "Bad value: '%s', logging enabled should be True/False." % req.logging_enabled, req.request_id)

class MessageValidator(ValidatorBase):
    @staticmethod
    def sendmessage_attr_validate(req, req_id):
        #type
        ValidatorBase.is_str(req.message_body, None, req_id)
        ValidatorBase.type_validate(req.delay_seconds, int, None, req_id)
        ValidatorBase.type_validate(req.priority, int, None, req_id)

        #value
        if req.message_body == "":
            raise MNSClientParameterException("MessageBodyInvalid", "Bad value: '', message body should not be ''.", req_id)

        if req.delay_seconds != -1 and req.delay_seconds < 0:
            raise MNSClientParameterException("DelaySecondsInvalid", "Bad value: '%d', delay_seconds should larger than 0." % req.delay_seconds, req_id)

        if req.priority != -1 and req.priority < 0:
            raise MNSClientParameterException("PriorityInvalid", "Bad value: '%d', priority should larger than 0." % req.priority, req_id)

    @staticmethod
    def receiphandle_validate(receipt_handle, req_id):
        if (receipt_handle == ""):
            raise MNSClientParameterException("ReceiptHandleInvalid", "The receipt handle should not be null.", req_id)

    @staticmethod
    def waitseconds_validate(wait_seconds, req_id):
        if wait_seconds != -1 and wait_seconds < 0:
            raise MNSClientParameterException("WaitSecondsInvalid", "Bad value: '%d', wait_seconds should larger than 0." % wait_seconds, req_id)

    @staticmethod
    def batchsize_validate(batch_size, req_id):
        if batch_size != -1 and batch_size < 0:
            raise MNSClientParameterException("BatchSizeInvalid", "Bad value: '%d', batch_size should larger than 0." % batch_size, req_id)

    @staticmethod
    def publishmessage_attr_validate(req):
        #type
        ValidatorBase.is_str(req.message_body, "message_body", req_id=req.request_id)
        ValidatorBase.is_str(req.message_tag, "message_tag", req_id=req.request_id)
        if req.direct_mail is not None:
            ValidatorBase.is_str(req.direct_mail.account_name, "account_name of direct mail", req_id=req.request_id)
            ValidatorBase.is_str(req.direct_mail.subject, "subject of direct mail", req_id=req.request_id)

        #value
        if req.message_body == "":
            raise MNSClientParameterException("MessageBodyInvalid", "Bad value: '', message body should not be ''.", req.request_id)
        if len(req.message_tag) > 16:
            raise MNSClientParameterException("MessageTagInvalid", "The length of message tag should be between 1 and 16.", req.request_id)

class CreateQueueValidator(QueueValidator):
    @staticmethod
    def validate(req):
        QueueValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        QueueValidator.queue_validate(req)

class DeleteQueueValidator(QueueValidator):
    @staticmethod
    def validate(req):
        QueueValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)

class ListQueueValidator(QueueValidator):
    @staticmethod
    def validate(req):
        QueueValidator.validate(req)
        QueueValidator.list_condition_validate(req)

class SetQueueAttrValidator(QueueValidator):
    @staticmethod
    def validate(req):
        QueueValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        QueueValidator.queue_validate(req)

class GetQueueAttrValidator(QueueValidator):
    @staticmethod
    def validate(req):
        QueueValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)

class SendMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.sendmessage_attr_validate(req, req.request_id)

class BatchSendMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        for entry in req.message_list:
            MessageValidator.sendmessage_attr_validate(entry, req.request_id)

class ReceiveMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.waitseconds_validate(req.wait_seconds, req.request_id)

class BatchReceiveMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.batchsize_validate(req.batch_size, req.request_id)
        MessageValidator.waitseconds_validate(req.wait_seconds, req.request_id)

class DeleteMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.receiphandle_validate(req.receipt_handle, req.request_id)

class BatchDeleteMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        for receipt_handle in req.receipt_handle_list:
            MessageValidator.receiphandle_validate(receipt_handle, req.request_id)

class PeekMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)

class BatchPeekMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.batchsize_validate(req.batch_size, req.request_id)

class ChangeMsgVisValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.queue_name, "queue_name", req.request_id)
        MessageValidator.receiphandle_validate(req.receipt_handle, req.request_id)
        if (req.visibility_timeout < 0 or req.visibility_timeout > 43200 ):
            raise MNSClientParameterException("VisibilityTimeoutInvalid", "Bad value: '%d', visibility timeout should between 0 and 43200." % req.visibility_timeout, req.request_id)

class TopicValidator(ValidatorBase):
    @staticmethod
    def topic_validate(req):
        #type
        ValidatorBase.type_validate(req.maximum_message_size, int, "maximum_message_size", req_id=req.request_id)

        #value
        if req.maximum_message_size != -1 and req.maximum_message_size <= 0:
            raise MNSClientParameterException("TopicAttrInvalid", "Bad value: '%s', maximum message size should larger than 0." % req.maximum_message_size, req.request_id)
        if req.logging_enabled != None and str(req.logging_enabled).lower() not in ("true", "false"):
            raise MNSClientParameterException("TopicAttrInvalid", "Bad value: '%s', logging enabled should be True/False." % req.logging_enabled, req.request_id)

class CreateTopicValidator(TopicValidator):
    @staticmethod
    def validate(req):
        TopicValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        TopicValidator.topic_validate(req)

class DeleteTopicValidator(TopicValidator):
    @staticmethod
    def validate(req):
        TopicValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)

class ListTopicValidator(TopicValidator):
    @staticmethod
    def validate(req):
        TopicValidator.validate(req)
        TopicValidator.list_condition_validate(req)

class SetTopicAttrValidator(TopicValidator):
    @staticmethod
    def validate(req):
        TopicValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        TopicValidator.topic_validate(req)

class GetTopicAttrValidator(TopicValidator):
    @staticmethod
    def validate(req):
        TopicValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)

class PublishMessageValidator(MessageValidator):
    @staticmethod
    def validate(req):
        MessageValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        MessageValidator.publishmessage_attr_validate(req)

class SubscriptionValidator(TopicValidator):
    @staticmethod
    def subscription_validate(req):
        TopicValidator.is_str(req.endpoint, "endpoint", req_id=req.request_id)
        TopicValidator.is_str(req.notify_strategy, "notify_strategy", req_id=req.request_id)
        TopicValidator.is_str(req.filter_tag, "filter_tag", req_id=req.request_id)
        TopicValidator.is_str(req.notify_content_format, "notify_content_format", req_id=req.request_id)

    @staticmethod
    def filter_tag_validate(filter_tag, req_id):
        if len(filter_tag) > 16:
            raise MNSClientParameterException("FilterTagInvalid", "Bad value: '%s', The length of filter tag should be between 1 and 16." % (filter_tag))

class SubscribeValidator(SubscriptionValidator):
    @staticmethod
    def validate(req):
        SubscriptionValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        ValidatorBase.name_validate(req.subscription_name, "subscription_name", req.request_id)
        SubscriptionValidator.subscription_validate(req)
        SubscriptionValidator.filter_tag_validate(req.filter_tag, req.request_id)

class UnsubscribeValidator(SubscriptionValidator):
    @staticmethod
    def validate(req):
        SubscriptionValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        ValidatorBase.name_validate(req.subscription_name, "subscription_name", req.request_id)

class ListSubscriptionByTopicValidator(SubscriptionValidator):
    @staticmethod
    def validate(req):
        SubscriptionValidator.validate(req)
        SubscriptionValidator.list_condition_validate(req)

class SetSubscriptionAttrValidator(SubscriptionValidator):
    @staticmethod
    def validate(req):
        SubscriptionValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        ValidatorBase.name_validate(req.subscription_name, "subscription_name", req.request_id)
        SubscriptionValidator.subscription_validate(req)

class GetSubscriptionAttrValidator(SubscriptionValidator):
    @staticmethod
    def validate(req):
        SubscriptionValidator.validate(req)
        ValidatorBase.name_validate(req.topic_name, "topic_name", req.request_id)
        ValidatorBase.name_validate(req.subscription_name, "subscription_name", req.request_id)
