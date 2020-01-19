# @Author  : yanchunhuo
# @Time    : 2020/1/19 14:33
from base.read_httpserver_config import Read_Http_Server_Config
import multiprocessing
import platform
import subprocess

def start_http_server(port):
    try:
        subprocess.check_output('python3 -m http.server '+port,shell=True)
    except:
        subprocess.check_output('python -m http.server ' + port, shell=True)

def http_server_init():
    httpserver_config = Read_Http_Server_Config().httpserver_config
    port = httpserver_config.httpserver_port
    if "windows"==platform.system().lower():
        pass
    elif "linux"==platform.system().lower():
        get_httpserver_process_ids_command = "ps -ef|grep 'http.server %s'|grep -v grep|awk '{print $2}'"%port
        httpserver_process_ids = subprocess.check_output(get_httpserver_process_ids_command, shell=True)
        if httpserver_process_ids:
            return
    elif "darwin"==platform.system().lower():
        pass
    p = multiprocessing.Process(target=start_http_server,args=(port,))
    p.daemon = True
    p.start()
