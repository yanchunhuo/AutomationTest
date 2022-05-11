#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class MNSExceptionBase(Exception):
    """
    @type type: string
    @param type: 错误类型

    @type message: string
    @param message: 错误描述

    @type req_id: string
    @param req_id: 请求的request_id
    """
    def __init__(self, type, message, req_id = None):
        self.type = type
        self.message = message
        self.req_id = req_id

    def get_info(self):
        if self.req_id is not None:
            return "(\"%s\" \"%s\") RequestID:%s\n" % (self.type, self.message, self.req_id)
        else:
            return "(\"%s\" \"%s\")\n" % (self.type, self.message)

    def __str__(self):
        return "MNSExceptionBase  %s" % (self.get_info())

class MNSClientException(MNSExceptionBase):
    def __init__(self, type, message, req_id = None):
        MNSExceptionBase.__init__(self, type, message, req_id)

    def __str__(self):
        return "MNSClientException  %s" % (self.get_info())

class MNSServerException(MNSExceptionBase):
    """ mns处理异常

        @note: 根据type进行分类处理，常见错误类型：
             : InvalidArgument       参数不合法
             : AccessDenied          无权对该资源进行当前操作
             : QueueNotExist         队列不存在
             : MessageNotExist       队列中没有消息
             : 更多错误类型请移步阿里云消息和通知服务官网进行了解；
    """
    def __init__(self, type, message, request_id, host_id, sub_errors=None):
        MNSExceptionBase.__init__(self, type, message, request_id)
        self.request_id = request_id
        self.host_id = host_id
        self.sub_errors = sub_errors

    def __str__(self):
        return "MNSServerException  %s" % (self.get_info())
        
class MNSClientNetworkException(MNSClientException):
    """ 网络异常

        @note: 检查endpoint是否正确、本机网络是否正常等;
    """
    def __init__(self, type, message, req_id=None):
        MNSClientException.__init__(self, type, message, req_id)

    def get_info(self):
        return "(\"%s\", \"%s\")\n" % (self.type, self.message)

    def __str__(self):
        return "MNSClientNetworkException  %s" % (self.get_info())

class MNSClientParameterException(MNSClientException):
    """ 参数格式错误

        @note: 请根据提示修改对应参数;
    """
    def __init__(self, type, message, req_id=None):
        MNSClientException.__init__(self, type, message, req_id)

    def __str__(self):
        return "MNSClientParameterException  %s" % (self.get_info())
