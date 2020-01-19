# @Author  : yanchunhuo
# @Time    : 2020/1/19 14:46
import socket

class Network:
    @classmethod
    def get_local_ip(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host = s.getsockname()[0]
            return host
        except:
            print('通过UDP协议获取IP出错')
            hostname=socket.gethostname()
            host=socket.gethostbyname(hostname)
        return host