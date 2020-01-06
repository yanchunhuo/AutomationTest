# @Author  : yanchunhuo
# @Time    : 2020/1/6 9:37
from locust import TaskSet,task,between
from locust.contrib.fasthttp import FastHttpLocust
import queue

class UserAction(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def index(self):
        try:
            if self.locust.num_queue.get()!=0:
                self.client.get('/')
        except queue.Empty:
            pass

class User(FastHttpLocust):
    wait_time=between(0,0)
    task_set=UserAction
    #控制每个从节点执行的次数
    excute_num=100
    num_queue=queue.Queue()
    for i in range(excute_num+1):
        num_queue.put_nowait(i)