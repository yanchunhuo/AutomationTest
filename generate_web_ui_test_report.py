#
# generate_web_ui_test_report.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2021-04-13T10:59:18.033Z+08:00
# @last-modified 2024-02-03T11:15:41.884Z+08:00
#

from base.read_report_config import ReadReportConfig
from common.str_tool import StrTool
from common.custom_multiprocessing import Custom_Pool
from common.date_time_tool import DateTimeTool
from common.mail_client import MailClient
from common.network import Network
import argparse
import platform
import subprocess

def generate_windows_reports(report_dir,test_time,port):
    generate_report_command='allure generate %s/report_data -o %s/report/web_ui_report_%s'%(report_dir,report_dir,test_time)
    subprocess.check_output(generate_report_command,shell=True)
    open_report_command='start cmd.exe @cmd /c "allure open -p %s %s/report/web_ui_report_%s"'%(port,report_dir,test_time)
    subprocess.check_output(open_report_command,shell=True)

def mail_notification(subject:str,content:str,to_mails:str):
    if not to_mails:
        return
    report_config = ReadReportConfig().report_config
    mail_client=MailClient(smtp_host=report_config['notification']['mail_smtp_host'],
                           smtp_port=report_config['notification']['mail_smtp_port'],
                           mail=report_config['notification']['mail'],
                           mail_password=report_config['notification']['mail_password'],
                           mail_from_name='WEB UI自动化测试',
                           is_ssl=report_config['notification']['mail_use_ssl'])
    mail_client.send_mail(to_mails=to_mails,subject=subject,content=content)
    print('%s 报告已发送邮件给:%s'%(DateTimeTool.get_now_time(),to_mails))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-ep', '--edge_port', help='edge生成报告使用的端口', type=str)
    parser.add_argument('-cp', '--chrome_port', help='chrome生成报告使用的端口', type=str)
    parser.add_argument('-fp', '--firefox_port', help='firefox生成报告使用的端口', type=str)
    parser.add_argument('-m','--mails',help='报告发送的邮件,多个邮件使用逗号隔开.发送邮件需先配置confing/report.yaml中配置邮件相关信息')
    report_config = ReadReportConfig().report_config
    args=parser.parse_args()
    if args.edge_port:
        edgeport=args.edge_port
    else:
        edgeport=report_config['web_ui']['web_ui_edge_port']
    if args.chrome_port:
        chromeport=args.chrome_port
    else:
        chromeport=report_config['web_ui']['web_ui_chrome_port']
    if args.firefox_port:
        firefoxport=args.firefox_port
    else:
        firefoxport=report_config['web_ui']['web_ui_firefox_port']
    if args.mails:
        to_mails=args.mails
    else:
        to_mails=''
    test_time=DateTimeTool.get_now_time('%Y_%m_%d_%H_%M_%S_%f')
    notice_title='%s WEB UI测试报告'%test_time
    notice_content=''
    if 'Windows' == platform.system():
        # 初始化进程池
        p_pool = Custom_Pool(3)
        if edgeport:
            # 获得当前监听edge端口的进程id
            get_edgeport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % edgeport
            try:
                get_allure_process_id=subprocess.check_output(get_edgeport_process_id_command, shell=True)
                get_allure_process_id=get_allure_process_id.decode('utf-8')
                get_allure_process_id=StrTool.get_str_with_lb_rb(get_allure_process_id, 'LISTENING', '\r\n').strip()
                kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                try:
                    subprocess.check_call(kill_allure_process_command,shell=True)
                except:
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),get_allure_process_id,edgeport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.get_now_time(),edgeport))
            print('%s生成edge报告,使用端口%s'%(DateTimeTool.get_now_time(),edgeport))
            print('%sedge报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), edgeport))
            notice_content += 'Edge WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), edgeport)
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/edge',test_time,edgeport))
        if chromeport:
            # 获得当前监听chrome端口的进程id
            get_chromeport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % chromeport
            try:
                get_allure_process_id=subprocess.check_output(get_chromeport_process_id_command, shell=True)
                get_allure_process_id=get_allure_process_id.decode('utf-8')
                get_allure_process_id=StrTool.get_str_with_lb_rb(get_allure_process_id, 'LISTENING', '\r\n').strip()
                kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                try:
                    subprocess.check_call(kill_allure_process_command,shell=True)
                except:
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),get_allure_process_id,chromeport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.get_now_time(),chromeport))
            print('%s生成chrome报告,使用端口%s'%(DateTimeTool.get_now_time(),chromeport))
            print('%schrome报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), chromeport))
            notice_content += 'Chrome WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), chromeport)
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/chrome',test_time,chromeport))
        if firefoxport:
            # 获得当前监听edge端口的进程id
            get_firefoxport_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % firefoxport
            try:
                get_allure_process_id=subprocess.check_output(get_firefoxport_process_id_command, shell=True)
                get_allure_process_id=get_allure_process_id.decode('utf-8')
                get_allure_process_id=StrTool.get_str_with_lb_rb(get_allure_process_id, 'LISTENING', '\r\n').strip()
                kill_allure_process_command='taskkill /F /pid %s'%get_allure_process_id
                try:
                    subprocess.check_call(kill_allure_process_command,shell=True)
                except:
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),get_allure_process_id,firefoxport))
            except:
                print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.get_now_time(),firefoxport))
            print('%s生成firefox报告,使用端口%s'%(DateTimeTool.get_now_time(),firefoxport))
            print('%sfirefox报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), firefoxport))
            notice_content += 'FireFox WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), firefoxport)
            p = p_pool.apply_async(generate_windows_reports,('output/web_ui/firefox',test_time,firefoxport))
        mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)
        p_pool.close()
        p_pool.join()
    else:
        # 获得当前allure所有进程id
        get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
        allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True)
        allure_process_ids = allure_process_ids.decode('utf-8')
        allure_process_ids = allure_process_ids.split('\n')
        if edgeport:
            # 获得当前监听edge端口的进程id
            get_edgeport_process_ids_command = "netstat -anp|grep -i "+edgeport+"|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
            edgeport_process_ids = subprocess.check_output(get_edgeport_process_ids_command,shell=True)
            edgeport_process_ids = edgeport_process_ids.decode('utf-8')
            edgeport_process_ids = edgeport_process_ids.split('\n')
            is_find = False
            for edgeport_process_id in edgeport_process_ids:
                if is_find:
                    break
                for allure_process_id in allure_process_ids:
                    allure_process_id = allure_process_id.strip()
                    edgeport_process_id = edgeport_process_id.strip()
                    if allure_process_id == edgeport_process_id and not is_find and allure_process_id and edgeport_process_id:
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),allure_process_id.strip(),edgeport))
                        subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                        is_find =True
                        break
            print('%s生成edge报告,使用端口%s'%(DateTimeTool.get_now_time(),edgeport))
            print('%sedge报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), edgeport))
            notice_content += 'Edge WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), edgeport)
            generate_report_command='allure generate output/web_ui/edge/report_data -o output/web_ui/edge/report/web_ui_report_%s'%(test_time)
            subprocess.check_output(generate_report_command,shell=True)
            open_report_command='nohup allure open -p %s output/web_ui/edge/report/web_ui_report_%s >logs/generate_web_ui_test_edge_report_%s.log 2>&1 &'%(edgeport,test_time,test_time)
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
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),allure_process_id.strip(),chromeport))
                        subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                        is_find = True
                        break
            print('%s生成chrome报告,使用端口%s'%(DateTimeTool.get_now_time(),chromeport))
            print('%schromeport报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), chromeport))
            notice_content += 'Chrome WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), chromeport)
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
                        print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),allure_process_id.strip(),firefoxport))
                        subprocess.check_output("kill -9 " + allure_process_id, shell=True)
                        is_find = True
                        break
            print('%s生成firefox报告,使用端口%s'%(DateTimeTool.get_now_time(),firefoxport))
            print('%sfirefoxport报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), firefoxport))
            notice_content += 'FireFox WEB UI测试报告：http://%s:%s/\n' % (Network.get_local_ip(), firefoxport)
            generate_report_command='allure generate output/web_ui/firefox/report_data -o output/web_ui/firefox/report/web_ui_report_%s'%(test_time)
            subprocess.check_output(generate_report_command,shell=True)
            open_report_command='nohup allure open -p %s output/web_ui/firefox/report/web_ui_report_%s >logs/generate_web_ui_test_firefox_report_%s.log 2>&1 &'%(firefoxport,test_time,test_time)
            subprocess.check_output(open_report_command,shell=True)
        mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)