#
# robot.py
# @author yanchunhuo
# @description 
# @created 2022-02-07T16:27:32.733Z+08:00
# @last-modified 2022-02-12T21:56:54.813Z+08:00
# https://developer.work.weixin.qq.com/document/path/91770


from common.dateTimeTool import DateTimeTool
from common.httpclient.doRequest import DoRequest
import ujson

class Robot:
    def __init__(self,webhook:str):
        self.webhook=webhook
        self.doRequest=DoRequest(self.webhook)
        self.doRequest.setVerify(False)
        self.doRequest.setHeaders({'Content-Type':'application/json'})

    def send_by_text(self,content:str,atUserIds:list=(),atMobiles:list=()):
        """[summary]

        Args:
            content (str): [description]
            atUserIds (list, optional): userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list. Defaults to ().
            atMobiles (list, optional): 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人. Defaults to ().

        Returns:
            [type]: [description]
        """
        params={}
        params.update({'msgtype':'text'})
        if not isinstance(atUserIds,list):
            atUserIds=list(atUserIds)
        if not isinstance(atMobiles,list):
            atMobiles=list(atMobiles)
        params.update({'text':{'content':content,'mentioned_list':atUserIds,'mentioned_mobile_list':atMobiles}})
        params=ujson.dumps(params)
        # 发送文本
        httpResponseResult=self.doRequest.post_with_form('',params)
        return httpResponseResult

    def send_by_markdown(self,content:str):
        params = {}
        params.update({'msgtype': 'markdown'})
        params.update({'markdown': {'content': content}})
        params = ujson.dumps(params)
        # 发送文本
        httpResponseResult = self.doRequest.post_with_form('', params)
        return httpResponseResult