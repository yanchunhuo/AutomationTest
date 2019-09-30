#-*- coding:utf8 -*-
import argparse
import subprocess
import sys

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
        sys.exit('请指定报告使用的端口,查看帮助:python generateReport.py --help')
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

