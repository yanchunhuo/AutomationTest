#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import xml.dom.minidom
import sys
import base64
import string
import types
from xml.etree import ElementTree
from .mns_exception import *
from .mns_request import *
try:
    import json
except ImportError:
    import simplejson as json

XMLNS = "http://mns.aliyuncs.com/doc/v1/"
class EncoderBase:
    @staticmethod
    def insert_if_valid(item_name, item_value, invalid_value, data_dic):
        if item_value != invalid_value:
            data_dic[item_name] = item_value

    @staticmethod
    def list_to_xml(tag_name1, tag_name2, data_list):
        doc = xml.dom.minidom.Document()
        rootNode = doc.createElement(tag_name1)
        rootNode.attributes["xmlns"] = XMLNS
        doc.appendChild(rootNode)
        if data_list:
            for item in data_list:
                keyNode = doc.createElement(tag_name2)
                rootNode.appendChild(keyNode)
                keyNode.appendChild(doc.createTextNode(item))
        else:
            nullNode = doc.createTextNode("")
            rootNode.appendChild(nullNode)
        return doc.toxml("utf-8")

    @staticmethod
    def dic_to_xml(tag_name, data_dic):
        doc = xml.dom.minidom.Document()
        rootNode = doc.createElement(tag_name)
        rootNode.attributes["xmlns"] = XMLNS
        doc.appendChild(rootNode)
        if data_dic:
            for k,v in data_dic.items():
                keyNode = doc.createElement(k)
                if type(v) is dict:
                    for subkey,subv in v.items():
                        subNode = doc.createElement(subkey)
                        subNode.appendChild(doc.createTextNode(subv))
                        keyNode.appendChild(subNode)
                else:
                    #tmp = doc.createTextNode(v.decode('utf-8'))
                    tmp = doc.createTextNode(v)
                    keyNode.appendChild(tmp)
                    #keyNode.appendChild(doc.createTextNode(v))
                rootNode.appendChild(keyNode)
        else:
            nullNode = doc.createTextNode("")
            rootNode.appendChild(nullNode)
        return doc.toxml("utf-8")

    @staticmethod
    def listofdic_to_xml(root_tagname, sec_tagname, dataList):
        doc = xml.dom.minidom.Document()
        rootNode = doc.createElement(root_tagname)
        rootNode.attributes["xmlns"] = XMLNS
        doc.appendChild(rootNode)
        if dataList:
            for subData in dataList:
                secNode = doc.createElement(sec_tagname)
                rootNode.appendChild(secNode)
                if not subData:
                    nullNode = doc.createTextNode("")
                    secNode.appendChild(nullNode)
                    continue
                for k,v in subData.items():
                    keyNode = doc.createElement(k)
                    secNode.appendChild(keyNode)
                    keyNode.appendChild(doc.createTextNode(v))
        else:
            nullNode = doc.createTextNode("")
            rootNode.appendChild(nullNode)
        return doc.toxml("utf-8")

class SetAccountAttrEncoder(EncoderBase):
    @staticmethod
    def encode(data):
        account_attr = {}
        EncoderBase.insert_if_valid("LoggingBucket", data.logging_bucket, None, account_attr)
        return EncoderBase.dic_to_xml("Account", account_attr)

class QueueEncoder(EncoderBase):
    @staticmethod
    def encode(data, has_slice = True):
        queue = {}
        EncoderBase.insert_if_valid("VisibilityTimeout", str(data.visibility_timeout), "-1", queue)
        EncoderBase.insert_if_valid("MaximumMessageSize", str(data.maximum_message_size), "-1", queue)
        EncoderBase.insert_if_valid("MessageRetentionPeriod", str(data.message_retention_period), "-1", queue)
        EncoderBase.insert_if_valid("DelaySeconds", str(data.delay_seconds), "-1", queue)
        EncoderBase.insert_if_valid("PollingWaitSeconds", str(data.polling_wait_seconds), "-1", queue)

        logging_enabled = str(data.logging_enabled)
        if str(data.logging_enabled).lower() == "true":
            logging_enabled = "True"
        elif str(data.logging_enabled).lower() == "false":
            logging_enabled = "False"
        EncoderBase.insert_if_valid("LoggingEnabled", logging_enabled, "None", queue)
        return EncoderBase.dic_to_xml("Queue", queue)

class MessageEncoder(EncoderBase):
    @staticmethod
    def encode(data):
        message = {}
        if data.base64encode:
            #base64 only support str
            tmpbody = data.message_body.encode('utf-8')
            msgbody = base64.b64encode(tmpbody).decode('utf-8')
        else:
            #xml only support unicode when contains Chinese
            if sys.version > '3':
                msgbody = data.message_body
            else:
                msgbody = data.message_body.decode('utf-8') if isinstance(data.message_body, str) else data.message_body
        EncoderBase.insert_if_valid("MessageBody", msgbody, u"", message)
        EncoderBase.insert_if_valid("DelaySeconds", str(data.delay_seconds), u"-1", message)
        EncoderBase.insert_if_valid("Priority", str(data.priority), u"-1", message)
        return EncoderBase.dic_to_xml("Message", message)

class MessagesEncoder:
    @staticmethod
    def encode(message_list, base64encode):
        msglist = []
        for msg in message_list:
            item = {}
            if base64encode:
                #base64 only support str
                #tmpbody = msg.message_body.encode('utf-8') if isinstance(msg.message_body, unicode) else msg.message_body
                tmpbody = msg.message_body.encode('utf-8')
                msgbody = base64.b64encode(tmpbody).decode('utf-8')
            else:
                #xml only support unicode when contains Chinese
                if sys.version > '3':
                    msgbody = msg.message_body
                else:
                    msgbody = msg.message_body.decode('utf-8') if isinstance(msg.message_body, str) else msg.message_body
            EncoderBase.insert_if_valid("MessageBody", msgbody, u"", item)
            EncoderBase.insert_if_valid("DelaySeconds", str(msg.delay_seconds), u"-1", item)
            EncoderBase.insert_if_valid("Priority", str(msg.priority), u"-1", item)
            msglist.append(item)
        return EncoderBase.listofdic_to_xml(u"Messages", u"Message", msglist)

class TopicMessageEncoder:
    @staticmethod
    def encode(req):
        message = {}
        #xml only support unicode when contains Chinese
        msgbody = req.message_body
        EncoderBase.insert_if_valid("MessageBody", msgbody, "", message)
        EncoderBase.insert_if_valid("MessageTag", req.message_tag, "", message)
        msg_attr = {}
        if req.direct_mail is not None:
            msg_attr["DirectMail"] = json.dumps(req.direct_mail.get())
        if req.direct_sms is not None:
            msg_attr["DirectSMS"] = json.dumps(req.direct_sms.get())
        if msg_attr != {}:
            message["MessageAttributes"] = msg_attr
        return EncoderBase.dic_to_xml("Message", message)

class ReceiptHandlesEncoder:
    @staticmethod
    def encode(receipt_handle_list):
        return EncoderBase.list_to_xml("ReceiptHandles", "ReceiptHandle", receipt_handle_list)

class TopicEncoder(EncoderBase):
    @staticmethod
    def encode(data):
        topic = {}
        logging_enabled = str(data.logging_enabled)
        if str(data.logging_enabled).lower() == "true":
            logging_enabled = "True"
        elif str(data.logging_enabled).lower() == "false":
            logging_enabled = "False"
        EncoderBase.insert_if_valid("MaximumMessageSize", str(data.maximum_message_size), "-1", topic)
        EncoderBase.insert_if_valid("LoggingEnabled", logging_enabled, "None", topic)
        return EncoderBase.dic_to_xml("Topic", topic)

class SubscriptionEncoder(EncoderBase):
    @staticmethod
    def encode(data, set=False):
        subscription = {}
        EncoderBase.insert_if_valid("NotifyStrategy", data.notify_strategy, "", subscription)
        if not set:
            EncoderBase.insert_if_valid("Endpoint", data.endpoint, "", subscription)
            EncoderBase.insert_if_valid("FilterTag", data.filter_tag, "", subscription)
            EncoderBase.insert_if_valid("NotifyContentFormat", data.notify_content_format, "", subscription)
        return EncoderBase.dic_to_xml("Subscription", subscription)

#-------------------------------------------------decode-----------------------------------------------------#
class DecoderBase:
    @staticmethod
    def xml_to_nodes(tag_name, xml_data):
        if xml_data == "":
            raise MNSClientNetworkException("RespDataDamaged", "Xml data is \"\"!")

        try:
            dom = xml.dom.minidom.parseString(xml_data)
        except Exception:
            raise MNSClientNetworkException("RespDataDamaged", xml_data)

        nodelist = dom.getElementsByTagName(tag_name)
        if not nodelist:
            raise MNSClientNetworkException("RespDataDamaged", "No element with tag name '%s'.\nData:%s" % (tag_name, xml_data))

        return nodelist[0].childNodes

    @staticmethod
    def xml_to_dic(tag_name, xml_data, data_dic, req_id=None):
        try:
            for node in DecoderBase.xml_to_nodes(tag_name, xml_data):
                if node.nodeName != "#text":
                    if node.childNodes != []:
                        data_dic[node.nodeName] = node.firstChild.data
                    else:
                        data_dic[node.nodeName] = ""
        except MNSClientNetworkException as e:
            raise MNSClientNetworkException(e.type, e.message, req_id)

    @staticmethod
    def xml_to_listofdic(root_tagname, sec_tagname, xml_data, data_listofdic, req_id=None):
        try:
            for message in DecoderBase.xml_to_nodes(root_tagname, xml_data):
                if message.nodeName != sec_tagname:
                    continue

                data_dic = {}
                for property in message.childNodes:
                    if property.nodeName != "#text" and property.childNodes != []:
                        data_dic[property.nodeName] = property.firstChild.data
                data_listofdic.append(data_dic)
        except MNSClientNetworkException:
            raise MNSClientNetworkException(e.type, e.message, req_id)

class ListQueueDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, with_meta, req_id=None):
        queueurl_list = []
        queuemeta_list = []
        next_marker = u""
        if (xml_data != ""):
            try:
                root = ElementTree.fromstring(xml_data)
                namespace = root.tag[0:-6]
                queues = list(root.iter(namespace + "Queue"))
                for queue in queues:
                    queuemeta = {}
                    for node in queue:
                        nodename = node.tag[len(namespace):]
                        nodevalue = node.text.strip()
                        if nodename == "QueueURL" and len(nodevalue) > 0 :
                            queueurl_list.append(nodevalue)
                        if len(nodevalue) > 0:
                            queuemeta[nodename] = nodevalue
                    if with_meta:
                        queuemeta_list.append(queuemeta)

                marker = list(root.iter(namespace + "NextMarker"))
                for node in marker:
                    next_marker = node.text.strip()
            except Exception as err:
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        else:
            raise MNSClientNetworkException("RespDataDamaged", "Xml data is \"\"!", req_id)
        return queueurl_list, str(next_marker), queuemeta_list

class GetAccountAttrDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Account", xml_data, data_dic)
        key_list = ["LoggingBucket"]
        for key in key_list:
            if key not in data_dic:
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic

class GetQueueAttrDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Queue", xml_data, data_dic, req_id)
        key_list = ["ActiveMessages", "CreateTime", "DelayMessages", "DelaySeconds", "InactiveMessages", "LastModifyTime", "MaximumMessageSize", "MessageRetentionPeriod", "QueueName", "VisibilityTimeout", "PollingWaitSeconds", "LoggingEnabled"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic

class SendMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Message", xml_data, data_dic, req_id)
        key_list = ["MessageId", "MessageBodyMD5"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)

        receipt_handle = ""
        if "ReceiptHandle" in data_dic.keys():
            receipt_handle = data_dic["ReceiptHandle"]

        return data_dic["MessageId"], data_dic["MessageBodyMD5"], receipt_handle

class BatchSendMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_listofdic = []
        message_list = []
        DecoderBase.xml_to_listofdic("Messages", "Message", xml_data, data_listofdic, req_id)
        try:
            for data_dic in data_listofdic:
                entry = SendMessageResponseEntry()
                entry.message_id = data_dic["MessageId"]
                entry.message_body_md5 = data_dic["MessageBodyMD5"]
                message_list.append(entry)
        except Exception as err:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return message_list

    @staticmethod
    def decodeError(xml_data, req_id=None):
        try:
            return ErrorDecoder.decodeError(xml_data, req_id)
        except Exception:
            pass

        data_listofdic = []
        DecoderBase.xml_to_listofdic("Messages", "Message", xml_data, data_listofdic, req_id)
        if len(data_listofdic) == 0:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)

        errType = None
        errMsg = None
        key_list1 = sorted(["ErrorCode", "ErrorMessage"])
        key_list2 = sorted(["MessageId", "MessageBodyMD5"])
        for data_dic in data_listofdic:
            keys = sorted(data_dic.keys())
            if keys != key_list1 and keys != key_list2:
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
            if keys == key_list1 and errType is None:
                errType = data_dic["ErrorCode"]
                errMsg = data_dic["ErrorMessage"]
        return errType, errMsg, None, None, data_listofdic

class RecvMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, base64decode, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Message", xml_data, data_dic, req_id)
        key_list = ["DequeueCount", "EnqueueTime", "FirstDequeueTime", "MessageBody", "MessageId", "MessageBodyMD5", "NextVisibleTime", "ReceiptHandle", "Priority"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        if base64decode:
            decode_str = base64.b64decode(data_dic["MessageBody"])
            data_dic["MessageBody"] = decode_str
        return data_dic

class BatchRecvMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, base64decode, req_id=None):
        data_listofdic = []
        message_list = []
        DecoderBase.xml_to_listofdic("Messages", "Message", xml_data, data_listofdic, req_id)
        try:
            for data_dic in data_listofdic:
                msg = ReceiveMessageResponseEntry()
                if base64decode:
                    msg.message_body = base64.b64decode(data_dic["MessageBody"])
                else:
                    msg.message_body = data_dic["MessageBody"]
                msg.dequeue_count = int(data_dic["DequeueCount"])
                msg.enqueue_time = int(data_dic["EnqueueTime"])
                msg.first_dequeue_time = int(data_dic["FirstDequeueTime"])
                msg.message_id = data_dic["MessageId"]
                msg.message_body_md5 = data_dic["MessageBodyMD5"]
                msg.priority = int(data_dic["Priority"])
                msg.next_visible_time = int(data_dic["NextVisibleTime"])
                msg.receipt_handle = data_dic["ReceiptHandle"]
                message_list.append(msg)
        except Exception as err:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return message_list

class PeekMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, base64decode, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Message", xml_data, data_dic, req_id)
        key_list = ["DequeueCount", "EnqueueTime", "FirstDequeueTime", "MessageBody", "MessageId", "MessageBodyMD5", "Priority"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        if base64decode:
            decode_str = base64.b64decode(data_dic["MessageBody"])
            data_dic["MessageBody"] = decode_str
        return data_dic

class BatchPeekMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, base64decode, req_id=None):
        data_listofdic = []
        message_list = []
        DecoderBase.xml_to_listofdic("Messages", "Message", xml_data, data_listofdic, req_id)
        try:
            for data_dic in data_listofdic:
                msg = PeekMessageResponseEntry()
                if base64decode:
                    msg.message_body = base64.b64decode(data_dic["MessageBody"])
                else:
                    msg.message_body = data_dic["MessageBody"]
                msg.dequeue_count = int(data_dic["DequeueCount"])
                msg.enqueue_time = int(data_dic["EnqueueTime"])
                msg.first_dequeue_time = int(data_dic["FirstDequeueTime"])
                msg.message_id = data_dic["MessageId"]
                msg.message_body_md5 = data_dic["MessageBodyMD5"]
                msg.priority = int(data_dic["Priority"])
                message_list.append(msg)
        except Exception as err:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return message_list

class BatchDeleteMessageDecoder(DecoderBase):
    @staticmethod
    def decodeError(xml_data, req_id=None):
        try:
            return ErrorDecoder.decodeError(xml_data, req_id)
        except Exception:
            pass

        data_listofdic = []
        DecoderBase.xml_to_listofdic("Errors", "Error", xml_data, data_listofdic, req_id)
        if len(data_listofdic) == 0:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)

        key_list = sorted(["ErrorCode", "ErrorMessage", "ReceiptHandle"])
        for data_dic in data_listofdic:
            for key in key_list:
                keys = sorted(data_dic.keys())
                if keys != key_list:
                    raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_listofdic[0]["ErrorCode"], data_listofdic[0]["ErrorMessage"], None, None, data_listofdic

class ChangeMsgVisDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("ChangeVisibility", xml_data, data_dic, req_id)

        if "ReceiptHandle" in data_dic.keys() and "NextVisibleTime" in data_dic.keys():
            return data_dic["ReceiptHandle"], data_dic["NextVisibleTime"]
        else:
            raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)

class ListTopicDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, with_meta, req_id=None):
        topicurl_list = []
        topicmeta_list = []
        next_marker = ""
        if (xml_data != ""):
            try:
                root = ElementTree.fromstring(xml_data)
                namespace = root.tag[0:-6]
                topics = list(root.iter(namespace + "Topic"))
                for topic in topics:
                    topicMeta = {}
                    for node in topic:
                        nodeName = node.tag[len(namespace):]
                        nodeValue = node.text.strip()
                        if nodeName == "TopicURL" and len(nodeValue) > 0:
                            topicurl_list.append(nodeValue)
                        if len(nodeValue) > 0:
                            topicMeta[nodeName] = nodeValue
                    if with_meta:
                        topicmeta_list.append(topicMeta)

                marker = list(root.iter(namespace + "NextMarker"))
                for node in marker:
                    next_marker = node.text.strip()
            except Exception as err:
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        else:
            raise MNSClientNetworkException("RespDataDamaged", "Xml data is \"\"!", req_id)
        return topicurl_list, str(next_marker), topicmeta_list

class GetTopicAttrDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Topic", xml_data, data_dic, req_id)
        key_list = ["MessageCount", "CreateTime", "LastModifyTime", "MaximumMessageSize", "MessageRetentionPeriod", "TopicName", "LoggingEnabled"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic

class PublishMessageDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Message", xml_data, data_dic, req_id)
        key_list = ["MessageId", "MessageBodyMD5"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic["MessageId"], data_dic["MessageBodyMD5"]

class ListSubscriptionByTopicDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        subscriptionurl_list = []
        next_marker = ""
        if (xml_data != ""):
            try:
                root = ElementTree.fromstring(xml_data)
                namespace = root.tag[0:-13]
                subscriptions = list(root.iter(namespace + "Subscription"))
                for subscription in subscriptions:
                    for node in subscription:
                        nodeName = node.tag[len(namespace):]
                        nodeValue = node.text.strip()
                        if nodeName == "SubscriptionURL" and len(nodeValue) > 0:
                            subscriptionurl_list.append(nodeValue)
                marker = list(root.iter(namespace + "NextMarker"))
                for node in marker:
                    next_marker = node.text.strip()
            except Exception:
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        else:
            raise MNSClientNetworkException("RespDataDamaged", "Xml data is \"\"!", req_id)
        return subscriptionurl_list, str(next_marker)

class GetSubscriptionAttrDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Subscription", xml_data, data_dic, req_id)
        key_list = ["TopicOwner", "TopicName", "SubscriptionName", "Endpoint", "NotifyStrategy", "NotifyContentFormat", "CreateTime", "LastModifyTime"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic

class ErrorDecoder(DecoderBase):
    @staticmethod
    def decodeError(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("Error", xml_data, data_dic, req_id)
        key_list = ["Code", "Message", "RequestId", "HostId"]
        for key in key_list:
            if key not in data_dic.keys():
                raise MNSClientNetworkException("RespDataDamaged", xml_data, req_id)
        return data_dic["Code"], data_dic["Message"], data_dic["RequestId"], data_dic["HostId"], None

class OpenServiceDecoder(DecoderBase):
    @staticmethod
    def decode(xml_data, req_id=None):
        data_dic = {}
        DecoderBase.xml_to_dic("OpenService", xml_data, data_dic, req_id)
        return data_dic
