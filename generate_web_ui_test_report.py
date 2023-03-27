#
# generate_web_ui_test_report.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2021-04-13T10:59:18.033Z+08:00
# @last-modified 2023-03-27T18:20:43.976Z+08:00
#

from base.read_report_config import Read_Report_Config
from common.strTool import StrTool
from common.custom_multiprocessing import Custom_Pool
from common.dateTimeTool import DateTimeTool
from common.network import Network
import argparse
import platform
import subprocess

def generate_windows_reports(report_dir,test_time,port):
    generate_report_command='allure generate %s/report_data -o %s/report/web_ui_report_%s'%(report_dir,report_dir,test_time)
    subprocess.check_output(generate_report_command,shell=True)
    open_report_command='start cmd.exe @cmd /c "allure open -p %s %s/report/web_ui_report_%s"'%(port,report_dir,test_time)
    subprocess.check_output(open_report_command,shell=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-ip', '--ie_port', help='ie生成报告使用的端口', type=str)
    parser.add_argument('-cp', '--chrome_port', help='chrome生成报告使用的端口', type=str)
    parser.add_argument('-fp', '--firefox_port', help='firefox生成报告使用的端口', type=str)
    args=parser.parse_args()
    report_config = Read_Report_Config().report_config
    if args.ie_port:
        ieport=args.ie_port
    else:
        ieport=report_config.web_ui_ie_port    
    if args.chrome_port:
        chromeport=args.chrome_port
    else:
        chromeport=report_config.web_ui_chrome_port
    if args.firefox_port:
        firefoxport=args.firefox_port
    else:
        firefoxport=report_config.web_ui_firefox_port
    test_time=DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
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
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),get_allure_process_id,ieport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),ieport))
            print('%s生成ie报告,使用端口%s'%(DateTimeTool.getNowTime(),ieport))
            print('%sie报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), ieport))
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/ie',test_time,ieport))
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
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),get_allure_process_id,chromeport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),chromeport))
            print('%s生成chrome报告,使用端口%s'%(DateTimeTool.getNowTime(),chromeport))
            print('%schrome报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), chromeport))
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/chrome',test_time,chromeport))
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
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),get_allure_process_id,firefoxport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),firefoxport))
            print('%s生成firefox报告,使用端口%s'%(DateTimeTool.getNowTime(),firefoxport))
            print('%sfirefox报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), firefoxport))
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/firefox',test_time,firefoxport))
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
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),allure_process_id.strip(),ieport))
                        subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                        is_find =True
                        break
            print('%s生成ie报告,使用端口%s'%(DateTimeTool.getNowTime(),ieport))
            print('%sie报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), ieport))
            generate_report_command='allure generate output/web_ui/ie/report_data -o output/web_ui/ie/report/web_ui_report_%s'%(test_time)
            subprocess.check_output(generate_report_command,shell=True)
            open_report_command='nohup allure open -p %s output/web_ui/ie/report/web_ui_report_%s >logs/generate_web_ui_test_ie_report_%s.log 2>&1 &'%(ieport,test_time,test_time)
            subprocess.check_output(open_report_command,shell=True)
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
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),allure_process_id.strip(),chromeport))
                        subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                        is_find = True
                        break
            print('%s生成chrome报告,使用端口%s'%(DateTimeTool.getNowTime(),chromeport))
            print('%schromeport报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), chromeport))
            generate_report_command='allure generate output/web_ui/chrome/report_data -o output/web_ui/chrome/report/web_ui_report_%s'%(test_time)
            subprocess.check_output(generate_report_command,shell=True)
            open_report_command='nohup allure open -p %s output/web_ui/chrome/report/web_ui_report_%s >logs/generate_web_ui_test_chrome_report_%s.log 2>&1 &'%(chromeport,test_time,test_time)
            subprocess.check_output(open_report_command,shell=True)
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
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),allure_process_id.strip(),firefoxport))
                        subprocess.check_output("kill -9 " + allure_process_id, shell=True)
                        is_find = True
                        break
            print('%s生成firefox报告,使用端口%s'%(DateTimeTool.getNowTime(),firefoxport))
            print('%sfirefoxport报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), firefoxport))
            generate_report_command='allure generate output/web_ui/firefox/report_data -o output/web_ui/firefox/report/web_ui_report_%s'%(test_time)
            subprocess.check_output(generate_report_command,shell=True)
            open_report_command='nohup allure open -p %s output/web_ui/firefox/report/web_ui_report_%s >logs/generate_web_ui_test_firefox_report_%s.log 2>&1 &'%(firefoxport,test_time,test_time)
            subprocess.check_output(open_report_command,shell=True)