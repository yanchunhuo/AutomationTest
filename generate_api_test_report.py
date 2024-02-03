#
# generate_api_test_report.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2021-04-13T10:59:17.953Z+08:00
# @last-modified 2024-02-03T11:14:49.305Z+08:00
#
from base.read_report_config import ReadReportConfig
from common.date_time_tool import DateTimeTool
from common.file_tool import FileTool
from common.mail_client import MailClient
from common.network import Network
from common.str_tool import StrTool
import argparse
import multiprocessing
import platform
import subprocess

def generate_windows_reports(test_time, port):
    generate_report_command='allure generate output/api/report_data -o output/api/report/api_report_%s'%(test_time)
    subprocess.check_output(generate_report_command,shell=True)
    open_report_command='start cmd.exe @cmd /c "allure open -p %s output/api/report/api_report_%s"'%(port,test_time)
    subprocess.check_output(open_report_command,shell=True)
    
def mail_notification(subject:str,content:str,to_mails:str):
    if not to_mails:
        return
    report_config = ReadReportConfig().report_config
    mail_client=MailClient(smtp_host=report_config['notification']['mail_smtp_host'],
                           smtp_port=report_config['notification']['mail_smtp_port'],
                           mail=report_config['notification']['mail'],
                           mail_password=report_config['notification']['mail_password'],
                           mail_from_name='API自动化测试',
                           is_ssl=report_config['notification']['mail_use_ssl'])
    mail_client.send_mail(to_mails=to_mails,subject=subject,content=content)
    print('%s 报告已发送邮件给:%s'%(DateTimeTool.get_now_time(),to_mails))
    
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='生成报告使用的端口', type=str)
    parser.add_argument('-m','--mails',help='报告发送的邮件,多个邮件使用逗号隔开.发送邮件需先配置confing/report.yaml中配置邮件相关信息')
    report_config = ReadReportConfig().report_config
    args=parser.parse_args()
    if args.port:
        port=args.port
    else:
        port = report_config['api']['api_port']
    if args.mails:
        to_mails=args.mails
    else:
        to_mails=''
    test_time=DateTimeTool.get_now_time('%Y_%m_%d_%H_%M_%S_%f')
    notice_title='%s API测试报告'%test_time
    notice_content='API测试报告地址：http://%s:%s/' % (Network.get_local_ip(), port)
    if 'Windows' == platform.system():
        get_allure_process_id_command = 'netstat -ano|findstr "0.0.0.0:%s"' % port
        try:
            get_allure_process_id = subprocess.check_output(get_allure_process_id_command, shell=True)
            get_allure_process_id = get_allure_process_id.decode('utf-8')
            get_allure_process_id = StrTool.get_str_with_lb_rb(get_allure_process_id, 'LISTENING', '\r\n').strip()
            kill_allure_process_command = 'taskkill /F /pid %s' % get_allure_process_id
            try:
                subprocess.check_call(kill_allure_process_command, shell=True)
            except:
                print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),get_allure_process_id,port))
        except:
            print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.get_now_time(),port))
        print('%s生成报告,使用端口%s'%(DateTimeTool.get_now_time(),port))
        print('%s报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), port))
        if report_config['notification']['is_enable_mail']:
            test_exit_code=FileTool.read_json_from_file('output/api/tmp/result.json')
            if report_config['notification']['is_only_emails_with_errors']:
                if not test_exit_code['result']==0:
                    mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)
            else:
                mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)
        process = multiprocessing.Process(target=generate_windows_reports, args=(test_time, port))
        process.start()
        process.join()
    else:
        # 获得当前allure所有进程id
        get_allure_process_ids_command = "ps -ef|grep -i allure\\.CommandLine|grep -v grep|awk '{print $2}'"
        allure_process_ids = subprocess.check_output(get_allure_process_ids_command, shell=True)
        allure_process_ids = allure_process_ids.decode('utf-8')
        allure_process_ids = allure_process_ids.split('\n')

        # 获得当前监听port端口的进程id
        get_port_process_ids_command = "netstat -anp|grep -i " + str(port) + "|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}'"
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
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.get_now_time(),allure_process_id.strip(),port))
                    subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                    is_find = True
                    break
        print('%s 生成报告,使用端口%s'%(DateTimeTool.get_now_time(),port))
        print('%s 报告地址:http://%s:%s/' % (DateTimeTool.get_now_time(),Network.get_local_ip(), port))
        if report_config['notification']['is_enable_mail']:
            test_exit_code=FileTool.read_json_from_file('output/api/tmp/result.json')
            if report_config['notification']['is_only_emails_with_errors']:
                if not test_exit_code['result']==0:
                    mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)
            else:
                mail_notification(subject=notice_title,content=notice_content,to_mails=to_mails)
        generate_report_command='allure generate output/api/report_data -o output/api/report/api_report_%s'%(test_time)
        subprocess.check_output(generate_report_command,shell=True)
        open_report_command='nohup allure open -p %s output/api/report/api_report_%s >logs/generate_api_test_report_%s.log 2>&1 &'%(port,test_time,test_time)
        subprocess.check_output(open_report_command,shell=True)