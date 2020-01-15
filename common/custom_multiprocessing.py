# @Author  : yanchunhuo
# @Time    : 2020/1/15 16:25

from multiprocessing.pool import Pool
import multiprocessing

class NoDaemonProcess(multiprocessing.Process):
    """
    重构multiprocessing.Process类，将进程始终定义为非守护进程
    """
    def _get_daemon(self):
        """
        总返回非守护进程属性值
        """
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)

class Custom_Pool(Pool):
    """
    重构multiprocessing.Pool类
    """
    Process = NoDaemonProcess