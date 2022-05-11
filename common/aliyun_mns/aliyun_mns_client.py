#
# aliyun_mns_client.py
# @author yanchunhuo
# @description 
# @created 2022-05-11T15:21:50.951Z+08:00
# @last-modified 2022-05-11T20:12:06.029Z+08:00
# Python SDK Version 1.1.6
from .mns.account import Account
from .mns.mns_common import TopicHelper
from .mns.queue import Message
from .mns.queue import QueueMeta
from .mns.subscription import SubscriptionMeta
from .mns.topic import TopicMessage
from .mns.topic import TopicMeta


class Aliyun_MNS_Client:
    def __init__(self, endpoint, access_key_id, access_key,token="",debug=False):
        self.account=Account(host=endpoint,access_id=access_key_id,access_key=access_key,security_token=token,debug=debug)
        self.account_id=endpoint.split("/")[2].split(".")[0]
        self.region=endpoint.split(".")[2]

    def get_queue(self,queue_name:str):
        """_summary_

        Args:
            queue_name (str): _description_

        Returns:
            _type_: Queue object
        """
        queue=self.account.get_queue(queue_name)
        return queue
    
    def create_queue(self,queue_name:str,queue_meta=None):
        """仅支持 字母、数字、- 的命名

        Args:
            queue_name (str): _description_
            queue_meta (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        queue=self.account.get_queue(queue_name)
        if queue_meta is None:
            queue_meta=QueueMeta()
        queue_url=queue.create(queue_meta=queue_meta)
        return queue_url
    
    def send_queue_message(self,queue_name:str,msg_body:str='',delay_seconds=None,priority=None):
        """_summary_

        Args:
            queue_name (str): _description_
            msg_body (str, optional): _description_. Defaults to ''.
            delay_seconds (_type_, optional): _description_. Defaults to None.
            priority (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: Message Ojbect
        """
        queue=self.account.get_queue(queue_name)
        message=Message(message_body=msg_body,delay_seconds=delay_seconds,priority=priority)
        result=queue.send_message(message=message)
        return result
    
    def receive_queue_message(self,queue_name:str,wait_seconds:int=-1,is_base64=False):
        """_summary_

        Args:
            queue_name (str): _description_
            wait_seconds (int, optional): _description_. Defaults to -1.

        Returns:
            _type_: Message Ojbect
        """
        queue=self.account.get_queue(queue_name)
        queue.set_encoding(is_base64)
        result=queue.receive_message(wait_seconds=wait_seconds)
        return result
    
    def delete_queue_message(self,queue_name:str,receipt_handle:str):
        queue=self.account.get_queue(queue_name)
        queue.delete_message(receipt_handle=receipt_handle)
    
    def delete_queue(self,queue_name:str):
        queue=self.account.get_queue(queue_name)
        queue.delete()
    
    def get_topic(self,topic_name:str):
        """

        Args:
            topic_name (str): _description_

        Returns:
            _type_: Topic Object
        """
        topic=self.account.get_topic(topic_name=topic_name)
        return topic
    
    def create_topic(self,topic_name:str,topic_meta=None,maximum_message_size=-1):
        """_summary_

        Args:
            topic_name (str): _description_
            topic_meta (_type_, optional): _description_. Defaults to None.
            maximum_message_size (int, optional): 字节数. Defaults to -1.

        Returns:
            _type_: _description_
        """
        topic=self.account.get_topic(topic_name=topic_name)
        if topic_meta is None:
            topic_meta=TopicMeta(maximum_message_size=maximum_message_size)
        topic_url=topic.create(topic_meta=topic_meta)
        return topic_url
    
    def create_topic_subscribe(self,subscribe_name:str,topic_name:str,queue_name:str,region:str=None,
                               notify_strategy="",notify_content_format="", filter_tag=""):
        topic=self.account.get_topic(topic_name=topic_name)
        subscribe=topic.get_subscription(subscription_name=subscribe_name)
        # 构建subscribe_meta
        if region is None:
            region=self.region
        queue_endpoint=TopicHelper.generate_queue_endpoint(region=region,accountid=self.account_id,queue_name=queue_name)
        subscribe_meta=SubscriptionMeta(endpoint=queue_endpoint,notify_strategy=notify_strategy,
                                        notify_content_format=notify_content_format, filter_tag=filter_tag)
        # 创建订阅
        topic_url=subscribe.subscribe(subscription_meta=subscribe_meta)
        return topic_url
    
    def send_topic_message(self,topic_name:str,msg_body:str='',message_tag:str="",direct_mail=None, direct_sms=None):
        """_summary_

        Args:
            topic_name (str): _description_
            msg_body (str, optional): _description_. Defaults to ''.
            message_tag (str, optional): _description_. Defaults to "".
            direct_mail (_type_, optional): _description_. Defaults to None.
            direct_sms (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: TopicMessage object
        """
        topic=self.account.get_topic(topic_name=topic_name)
        message=TopicMessage(message_body=msg_body,message_tag=message_tag,direct_mail=direct_mail,direct_sms=direct_sms)
        result=topic.publish_message(message=message)
        return result
    
    def delete_topic(self,topic_name:str):
        topic=self.account.get_topic(topic_name=topic_name)
        topic.delete()
    