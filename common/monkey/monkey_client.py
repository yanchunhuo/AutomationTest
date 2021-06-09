#
# monkey_client.py
# @author yanchunhuo
# @description 
# @created 2021-05-18T21:08:38.694Z+08:00
# @last-modified 2021-06-09T21:51:42.306Z+08:00
# github https://github.com/yanchunhuo
from common.dateTimeTool import DateTimeTool
import platform
import subprocess

class Monkey_Client:
    
    def start_android_monkey(self, udid: str, package: str, std_log_file_path: str, err_log_file_path,
                             throttle: int = 100,
                             event_times: int = 100000, ):
        start_command = 'adb -s %s shell monkey -p %s --throttle %s --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes --pct-syskeys 0 -v -v -v %s 1 >%s   2>%s' \
                        % (udid, package, int(throttle), int(event_times), std_log_file_path, err_log_file_path)
        sub_p = subprocess.Popen(start_command, shell=True)
        return sub_p
    
    def stop_android_monkey(self,udid:str,sub_p=None):
        if sub_p:
            sub_p.kill()
        #kill monkey
        monkey_process_id=''
        if 'Windows' == platform.system():
            get_monkey_process_id_command='adb -s %s shell ps|findstr monkey'%udid
            try:
                monkey_process_id=subprocess.check_output(get_monkey_process_id_command,shell=True)
                monkey_process_id = monkey_process_id.decode('utf-8')
            except:
                print('%s未查找到%s的monkey服务' %(DateTimeTool.getNowTime(),udid))
        else:
            get_monkey_process_id_command='adb -s %s shell ps|grep monkey'%udid
            try:
                monkey_process_id=subprocess.check_output(get_monkey_process_id_command,shell=True)
                monkey_process_id = monkey_process_id.decode('utf-8')
            except:
                print('%s未查找到%s的monkey服务' %(DateTimeTool.getNowTime(),udid))
        if monkey_process_id:
            get_lambda=lambda info:list(filter(None,info.split(' '))) if info else []
            monkey_process_id=get_lambda(monkey_process_id)
            monkey_process_id=monkey_process_id[1]
            kill_monkey_process_command='adb -s %s shell kill %s'%(udid,monkey_process_id)
            try:
                result=subprocess.check_call(kill_monkey_process_command,shell=True)
                print('%s关闭monkey进程,进程id:%s'%(DateTimeTool.getNowTime(),monkey_process_id))
                return result
            except:
                print('%s关闭monkey进程,进程id:%s'%(DateTimeTool.getNowTime(),monkey_process_id))
        