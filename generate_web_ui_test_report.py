#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36

from common.strTool import StrTool
from common.custom_multiprocessing import Custom_Pool
import argparse
import platform
import subprocess
import sys

def generate_windows_reports(report_dir,port):
    subprocess.check_output("start cmd.exe @cmd /c allure serve -p " + port + " " + report_dir, shell=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-ieport','--ieport',help='ie浏览器报告监听端口',type=str)
    parser.add_argument('-chromeport', '--chromeport', help='chrome浏览器报告监听端口', type=str)
    parser.add_argument('-firefoxport', '--firefoxport', help='friefox浏览器报告监听端口', type=str)
    args=parser.parse_args()

    ieport=args.ieport
    chromeport=args.chromeport
    firefoxport=args.firefoxport
    if not ieport and not chromeport and not firefoxport:
        sys.exit('请指定报告使用的端口,查看帮助:python generate_web_ui_test_report.py --help')
    else:
        if 'Windows' == platform.system():
            # 初始化进程池
            p_pool = Custom_Pool(3)
            if ieport:
                # 获得当前监听ie端口的进程id
                get_ieport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % ieport
                try:
                    get_allure_process_id=subprocess.check_output(get_ieport_process_id_command, shell=True)
                    get_allure_process_id=get_allure_process_id.decode('utf-8')
                    get_allure_process_id=StrTool.getStringWithLBRB(get_allure_process_id, 'LISTENING', '\r\n').strip()
                    kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                    try:
                        subprocess.check_call(kill_allure_process_command,shell=True)
                    except:
                        print('关闭allure进程,进程id:' + get_allure_process_id + ',该进程监听已监听端口:' + ieport)
                except:
                    print('allure未查找到监听端口%s的服务' % ieport)
                print('生成ie报告,使用端口' + ieport)
                p = p_pool.apply_async(generate_windows_reports,('output/web_ui/ie',ieport))
            if chromeport:
                # 获得当前监听chrome端口的进程id
                get_chromeport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % chromeport
                try:
                    get_allure_process_id=subprocess.check_output(get_chromeport_process_id_command, shell=True)
                    get_allure_process_id=get_allure_process_id.decode('utf-8')
                    get_allure_process_id=StrTool.getStringWithLBRB(get_allure_process_id, 'LISTENING', '\r\n').strip()
                    kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                    try:
                        subprocess.check_call(kill_allure_process_command,shell=True)
                    except:
                        print('关闭allure进程,进程id:' + get_allure_process_id + ',该进程监听已监听端口:' + chromeport)
                except:
                    print('allure未查找到监听端口%s的服务' % chromeport)
                print('生成chrome报告,使用端口' + chromeport)
                p = p_pool.apply_async(generate_windows_reports,('output/web_ui/chrome',chromeport))
            if firefoxport:
                # 获得当前监听ie端口的进程id
                get_firefoxport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % firefoxport
                try:
                    get_allure_process_id=subprocess.check_output(get_firefoxport_process_id_command, shell=True)
                    get_allure_process_id=get_allure_process_id.decode('utf-8')
                    get_allure_process_id=StrTool.getStringWithLBRB(get_allure_process_id, 'LISTENING', '\r\n').strip()
                    kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                    try:
                        subprocess.check_call(kill_allure_process_command,shell=True)
                    except:
                        print('关闭allure进程,进程id:' + get_allure_process_id + ',该进程监听已监听端口:' + firefoxport)
                except:
                    print('allure未查找到监听端口%s的服务' % firefoxport)
                print('生成firefox报告,使用端口' + firefoxport)
                p = p_pool.apply_async(generate_windows_reports,('output/web_ui/firefox',firefoxport))
            p_pool.close()
            p_pool.join()
        else:
            # 获得当前allure所有进程id
            get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
            allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True)
            allure_process_ids = allure_process_ids.decode('utf-8')
            allure_process_ids = allure_process_ids.split('\n')
            if ieport:
                # 获得当前监听ie端口的进程id
                get_ieport_process_ids_command = "netstat -anp|grep -i "+ieport+"|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
                ieport_process_ids = subprocess.check_output(get_ieport_process_ids_command,shell=True)
                ieport_process_ids = ieport_process_ids.decode('utf-8')
                ieport_process_ids = ieport_process_ids.split('\n')
                is_find = False
                for ieport_process_id in ieport_process_ids:
                    if is_find:
                        break
                    for allure_process_id in allure_process_ids:
                        allure_process_id = allure_process_id.strip()
                        ieport_process_id = ieport_process_id.strip()
                        if allure_process_id == ieport_process_id and not is_find and allure_process_id and ieport_process_id:
                            print('关闭allure进程,进程id:' + allure_process_id.strip() + ',该进程监听已监听端口:' + ieport)
                            subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                            is_find =True
                            break
                print('生成ie报告,使用端口'+ieport)
                subprocess.check_output("nohup allure serve -p " + ieport + " output/web_ui/ie >logs/ie_generate_web_ui_test_report.log 2>&1 &",shell=True)
            if chromeport:
                # 获得当前监听chrome端口的进程id
                get_chromeport_process_ids_command = "netstat -anp|grep -i " + chromeport + "|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
                chromeport_process_ids = subprocess.check_output(get_chromeport_process_ids_command, shell=True)
                chromeport_process_ids = chromeport_process_ids.decode('utf-8')
                chromeport_process_ids = chromeport_process_ids.split('\n')
                is_find = False
                for chromeport_process_id in chromeport_process_ids:
                    if is_find:
                        break
                    for allure_process_id in allure_process_ids:
                        allure_process_id = allure_process_id.strip()
                        chromeport_process_id =  chromeport_process_id.strip()
                        if allure_process_id == chromeport_process_id and not is_find and allure_process_id and chromeport_process_id:
                            print('关闭allure进程,进程id:' + allure_process_id.strip() + ',该进程监听已监听端口:' + chromeport)
                            subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                            is_find = True
                            break
                print('生成chrome报告,使用端口' + chromeport)
                subprocess.check_output("nohup allure serve -p " + chromeport + " output/web_ui/chrome >logs/chrome_generate_web_ui_test_report.log 2>&1 &",shell=True)
            if firefoxport:
                # 获得当前监听firefox端口的进程id
                get_firefoxport_process_ids_command = "netstat -anp|grep -i " + firefoxport + "|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
                firefoxport_process_ids = subprocess.check_output(get_firefoxport_process_ids_command, shell=True)
                firefoxport_process_ids = firefoxport_process_ids.decode('utf-8')
                firefoxport_process_ids = firefoxport_process_ids.split('\n')
                is_find = False
                for firefoxport_process_id in firefoxport_process_ids:
                    if is_find:
                        break
                    for allure_process_id in allure_process_ids:
                        allure_process_id = allure_process_id.strip()
                        firefoxport_process_id =  firefoxport_process_id.strip()
                        if allure_process_id == firefoxport_process_id and not is_find and allure_process_id and firefoxport_process_id:
                            print('关闭allure进程,进程id:'+allure_process_id.strip()+',该进程监听已监听端口:'+firefoxport)
                            subprocess.check_output("kill -9 " + allure_process_id, shell=True)
                            is_find = True
                            break
                print('生成firefox报告,使用端口' + firefoxport)
                subprocess.check_output("nohup allure serve -p " + firefoxport + " output/web_ui/firefox >logs/firefox_generate_web_ui_test_report.log 2>&1 &",shell=True)