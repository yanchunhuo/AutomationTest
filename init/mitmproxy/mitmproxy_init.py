# @Author  : yanchunhuo
# @Time    : 2020/7/15 17:43
# github https://github.com/yanchunhuo
from base.read_mitmproxy_config import Read_Mitmproxy_Config
from common.dateTimeTool import DateTimeTool
from common.strTool import StrTool
import multiprocessing
import platform
import subprocess

def start_mitmproxy(port,ssl_insecure):
    if 'Windows' == platform.system():
        if ssl_insecure:
            subprocess.check_output("start cmd.exe @cmd /c mitmdump -k -p %s -s %s "%(port,'init/mitmproxy/addons.py'), shell=True)
        else:
            subprocess.check_output("start cmd.exe @cmd /c mitmdump -p %s -s %s "%(port,'init/mitmproxy/addons.py'), shell=True)
    else:
        if ssl_insecure:
            subprocess.check_output('nohup mitmdump -k -p %s -s %s'%(port,'init/mitmproxy/addons.py >>logs/mitmproxy.log 2>&1 &'),shell=True)
        else:
            subprocess.check_output('nohup mitmdump -p %s -s %s'%(port,'init/mitmproxy/addons.py >>logs/mitmproxy.log 2>&1 &'),shell=True)

def mitmproxy_init():
    mitmproxy_config = Read_Mitmproxy_Config().mitmproxy_config
    port = mitmproxy_config.proxy_port
    ssl_insecure=mitmproxy_config.ssl_insecure
    if "windows"==platform.system().lower():
        get_mitmproxy_process_id_command='netstat -ano|findstr "0.0.0.0:%s"'%port
        try:
            mitmproxy_process_id = subprocess.check_output(get_mitmproxy_process_id_command, shell=True)
            mitmproxy_process_id = mitmproxy_process_id.decode('utf-8')
            mitmproxy_process_id = StrTool.getStringWithLBRB(mitmproxy_process_id, 'LISTENING', '\r\n').strip()
            kill_mitmproxy_process_command = 'taskkill /F /pid %s' % mitmproxy_process_id
            try:
                print('%s关闭mitmproxy进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),mitmproxy_process_id,port))
                subprocess.check_call(kill_mitmproxy_process_command, shell=True)
            except:
                print('%s关闭mitmproxy进程失败,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),mitmproxy_process_id,port))
        except:
            print('%smitmproxy未查找到监听端口%s的服务'%(DateTimeTool.getNowTime(),port))
    elif "linux"==platform.system().lower():
        # 获得当前mitmproxy所有进程id
        get_mitmproxy_process_ids_command = "ps -ef|grep 'mitmdump'|grep -v grep|awk '{print $2}'"
        try:
            mitmproxy_process_ids = subprocess.check_output(get_mitmproxy_process_ids_command, shell=True)
            mitmproxy_process_ids = mitmproxy_process_ids.decode('utf-8')
            get_lambda = lambda info: list(filter(None, info.split('\n'))) if info else []
            mitmproxy_process_ids = get_lambda(mitmproxy_process_ids)
            if not len(mitmproxy_process_ids)>0:
                print('%smitmproxy未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),port))
            for mitmproxy_process_id in mitmproxy_process_ids:
                try:
                    print('%s关闭mitmproxy进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),mitmproxy_process_id,port))
                    subprocess.check_output("kill -9 " + mitmproxy_process_id, shell=True)
                except:
                    print('%s关闭mitmproxy进程失败,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),mitmproxy_process_id,port))
        except:
            print('%smitmproxy未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),port))
    elif "darwin"==platform.system().lower():
        pass
    print('%s启动mitmproxy,使用端口%s'%(DateTimeTool.getNowTime(),port))
    p = multiprocessing.Process(target=start_mitmproxy,args=(port,ssl_insecure,))
    p.daemon = True
    p.start()