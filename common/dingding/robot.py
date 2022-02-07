#
# robot.py
# @author yanchunhuo
# @description 
# @created 2021-04-13T11:35:22.550Z+08:00
# @last-modified 2022-02-07T18:55:03.094Z+08:00
#

from common.dateTimeTool import DateTimeTool
from common.httpclient.doRequest import DoRequest
import hmac
import hashlib
import base64
import urllib.parse
import ujson

class Robot:
    def __init__(self,webhook:str,secret_key:str=None):
        self.webhook=webhook
        self.secret_key=secret_key
        self.doRequest=DoRequest(self.webhook)
        self.doRequest.setHeaders({'Content-Type':'application/json'})

    def _generator_sign(self,timestamp:str,secret_key:str):
        secret_key_enc = secret_key.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret_key)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_key_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_by_text(self,content:str,atMobiles:list=(),isAtAll=False):
        params={}
        params.update({'msgtype':'text'})
        params.update({'text':{'content':content}})
        at_params={}
        if not isinstance(atMobiles,list):
            atMobiles=list(atMobiles)
        at_params.update({'at':{'atMobiles':atMobiles,'isAtAll':isAtAll}})
        params.update(at_params)
        params=ujson.dumps(params)
        # 构造path
        path='/'
        if self.secret_key:
            timestamp = DateTimeTool.getNowTimeStampWithMillisecond()
            path='&timestamp={}&sign={}'.format(timestamp,self._generator_sign(timestamp,self.secret_key))
        # 发送文本
        httpResponseResult=self.doRequest.post_with_form(path,params)
        return httpResponseResult

    def send_by_markdown(self,title:str,text:str,atMobiles:list=(),isAtAll=False):
        params = {}
        params.update({'msgtype': 'markdown'})
        params.update({'markdown': {'title': title,'text':text}})
        at_params = {}
        if not isinstance(atMobiles, list):
            atMobiles = list(atMobiles)
        at_params.update({'at': {'atMobiles': atMobiles, 'isAtAll': isAtAll}})
        params.update(at_params)
        params = ujson.dumps(params)
        # 构造path
        path = '/'
        if self.secret_key:
            timestamp = DateTimeTool.getNowTimeStampWithMillisecond()
            path = '&timestamp={}&sign={}'.format(timestamp, self._generator_sign(timestamp, self.secret_key))
        # 发送文本
        httpResponseResult = self.doRequest.post_with_form(path, params)
        return httpResponseResult