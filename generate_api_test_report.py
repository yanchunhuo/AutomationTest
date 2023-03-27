#
# generate_api_test_report.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2021-04-13T10:59:17.953Z+08:00
# @last-modified 2023-03-27T18:00:22.416Z+08:00
#

from base.read_report_config import Read_Report_Config
from common.dateTimeTool import DateTimeTool
from common.dingding.robot import Robot
from common.qiyeweixin.robot import Robot as QiWei_Robot
from common.network import Network
from common.strTool import StrTool
import argparse
import multiprocessing
import platform
import subprocess

def generate_windows_reports(test_time, port):
    generate_report_command='allure generate output/api/report_data -o output/api/report/api_report_%s'%(test_time)
    subprocess.check_output(generate_report_command,shell=True)
    open_report_command='start cmd.exe @cmd /c "allure open -p %s output/api/report/api_report_%s"'%(port,test_time)
    subprocess.check_output(open_report_command,shell=True)

def notice(title: str, markdown_text: str, atMobiles: list = (), isAtAll=True):
    report_config = Read_Report_Config().report_config
    # 钉钉通知
    dingding_webhooks = report_config.dingding_webhooks
    dingding_secret_keys = report_config.dingding_secret_keys
    for i, dingding_webhook in enumerate(dingding_webhooks):
        dingding_secret_key = dingding_secret_keys[i]
        robot = Robot(dingding_webhook, dingding_secret_key)
        robot.send_by_markdown(title, markdown_text, atMobiles, isAtAll)
    # 企业微信通知
    qiyeweixin_webhooks = report_config.qiyeweixin_webhooks
    for i,qiyeweixin_webhook in enumerate(qiyeweixin_webhooks):
        qiwei_robot=QiWei_Robot(qiyeweixin_webhook)
        qiwei_robot.send_by_markdown(markdown_text)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='生成报告使用的端口', type=str)
    args=parser.parse_args()
    if args.port:
        port=args.port
    else:
        report_config = Read_Report_Config().report_config
        port = report_config.api_port
    notice_title = 'API自动化测试报告'
    test_time=DateTimeTool.getNowTime('%Y_%m_%d_%H_%M_%S_%f')
    notice_markdown_text = '* API生成时间：%s \n' % test_time
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
                print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),get_allure_process_id,port))
        except:
            print('%sallure未查找到监听端口%s的服务' % (DateTimeTool.getNowTime(),port))
        print('%s生成报告,使用端口%s'%(DateTimeTool.getNowTime(),port))
        print('%s报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), port))
        notice_markdown_text += '* [API自动化测试报告](http://%s:%s/)' % (Network.get_local_ip(), port)
        notice(notice_title, notice_markdown_text)
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
                    print('%s关闭allure进程,进程id:%s,该进程监听已监听端口:%s'%(DateTimeTool.getNowTime(),allure_process_id.strip(),port))
                    subprocess.check_output("kill -9 " + allure_process_id.strip(), shell=True)
                    is_find = True
                    break
        print('%s生成报告,使用端口%s'%(DateTimeTool.getNowTime(),port))
        print('%s报告地址:http://%s:%s/' % (DateTimeTool.getNowTime(),Network.get_local_ip(), port))
        notice_markdown_text += '* [API自动化测试报告](http://%s:%s/)' % (Network.get_local_ip(), port)
        notice(notice_title, notice_markdown_text)
        generate_report_command='allure generate output/api/report_data -o output/api/report/api_report_%s'%(test_time)
        subprocess.check_output(generate_report_command,shell=True)
        open_report_command='nohup allure open -p %s output/api/report/api_report_%s >logs/generate_api_test_report_%s.log 2>&1 &'%(port,test_time,test_time)
        subprocess.check_output(open_report_command,shell=True)