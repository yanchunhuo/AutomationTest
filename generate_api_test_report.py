# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
from common.strTool import StrTool
import argparse
import multiprocessing
import subprocess
import sys
import platform

def generate_windows_reports(report_dir,port):
    subprocess.check_output("start cmd.exe @cmd /c allure serve -p " + port + " " + report_dir, shell=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-p','--port',help='报告监听的端口',type=str)
    args=parser.parse_args()

    port = args.port
    if not port:
        sys.exit('请指定报告使用的端口,查看帮助:python generate_api_test_report.py --help')
    else:
        if 'Windows' == platform.system():
            get_allure_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % port
            try:
                get_allure_process_id = subprocess.check_output(get_allure_process_id_command, shell=True)
                get_allure_process_id = get_allure_process_id.decode('utf-8')
                get_allure_process_id = StrTool.getStringWithLBRB(get_allure_process_id, 'LISTENING', '\r\n').strip()
                kill_allure_process_command = 'taskkill /F /pid %s' % get_allure_process_id
                try:
                    subprocess.check_call(kill_allure_process_command, shell=True)
                except:
                    print('关闭allure进程,进程id:' + get_allure_process_id + ',该进程监听已监听端口:' + port)
            except:
                print('allure未查找到监听端口%s的服务' % port)
            print('生成报告,使用端口' + port)
            process=multiprocessing.Process(target=generate_windows_reports,args=('output/api/',port))
            process.start()
            process.join()
        else:
            # 获得当前allure所有进程id
            get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
            allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True)
            allure_process_ids = allure_process_ids.decode('utf-8')
            allure_process_ids = allure_process_ids.split('\n')

            # 获得当前监听port端口的进程id
            get_port_process_ids_command = "netstat -anp|grep -i " + port + "|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
            port_process_ids = subprocess.check_output(get_port_process_ids_command, shell=True)
            port_process_ids = port_process_ids.decode('utf-8')
            port_process_ids = port_process_ids.split('\n')
            is_find = False
            for port_process_id in port_process_ids:
                if is_find:
                    break
                for allure_process_id in allure_process_ids:
                    allure_process_id = allure_process_id.strip()
                    port_process_id = port_process_id.strip()
                    if allure_process_id == port_process_id and not is_find and allure_process_id and port_process_id:
                        print('关闭allure进程,进程id:' + allure_process_id.strip() + ',该进程监听已监听端口:' + port)
                        subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                        is_find = True
                        break
            print('生成报告,使用端口' + port)
            subprocess.check_output("nohup allure serve -p " + port + " output/api/ >logs/generate_api_test_report.log 2>&1 &",shell=True)

