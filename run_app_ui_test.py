#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.read_app_ui_config import Read_APP_UI_Config
from base.read_app_ui_devices_info import Read_APP_UI_Devices_Info
from common.httpclient.doRequest import DoRequest
from common.dateTimeTool import DateTimeTool
from common.fileTool import FileTool
from common.custom_multiprocessing import Custom_Pool
from common.pytest import deal_pytest_ini_file
from init.java.java_maven_init import java_maven_init
from init.httpserver.http_server_init import http_server_init
from init.mitmproxy.mitmproxy_init import mitmproxy_init
import argparse
import multiprocessing
import os
import pytest
import sys
import ujson

def pytest_main(pytest_execute_params):
    exit_code = pytest.main(pytest_execute_params)

def start_app_device_test(index,device_info,keyword,dir,markexpr,capture,reruns,lf,clr):
    for path, dirs, files in os.walk('config/app_ui_tmp'):
        for file in files:
            if(int(file)==index):
                os.rename(os.path.join(path,file),os.path.join(path,str(os.getpid())))

    print('%s开始检测appium server是否可用......'%DateTimeTool.getNowTime())
    try:
        doRquest = DoRequest('http://'+device_info['server_ip']+':%s/wd/hub'%device_info['server_port'].strip())
        httpResponseResult = doRquest.get('/status')
        result = ujson.loads(httpResponseResult.body)
        if result['status'] == 0:
            print('%sappium server状态为可用......'%DateTimeTool.getNowTime())
        else:
            sys.exit('%sappium server状态为不可用'%DateTimeTool.getNowTime())
    except:
        print('%sappium server状态为不可用'%DateTimeTool.getNowTime())
        raise Exception('%sappium server状态为不可用'%DateTimeTool.getNowTime())

    a_devices_desired_capabilities = device_info['capabilities']
    print('%s开始设备%s测试......'%(DateTimeTool.getNowTime(),device_info['device_desc']))
    print('%s当前设备所需测试的desired_capabilities为:%s'%(DateTimeTool.getNowTime(),a_devices_desired_capabilities))
    for desired_capabilities in a_devices_desired_capabilities:
        FileTool.writeObjectIntoFile(desired_capabilities,'config/app_ui_tmp/'+str(os.getpid())+'_current_desired_capabilities')
        desired_capabilities_desc=None
        if 'appPackage' in desired_capabilities.keys():
            desired_capabilities_desc = desired_capabilities['appPackage']
        elif 'app' in desired_capabilities.keys():
            desired_capabilities_desc = desired_capabilities['app'].split('/')[-1]
        elif 'bundleId' in desired_capabilities.keys():
            desired_capabilities_desc = desired_capabilities['bundleId']
        print('%s当前设备开始测试的desired_capabilities为:%s'%(DateTimeTool.getNowTime(),desired_capabilities))
        # 执行pytest前的参数准备
        pytest_execute_params = ['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/app_ui/%s/%s/report_data/'%(device_info['device_desc'],desired_capabilities_desc)]
        # 判断目录参数
        if not dir:
            dir = 'cases/app_ui/'
        # 判断关键字参数
        if keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(keyword)
        # 判断markexpr参数
        if markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(markexpr)
        # 判断是否输出日志
        if capture:
            if int(capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if reruns:
            if int(reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(reruns)
        # 判断是否只运行上一次失败的用例
        if lf:
            if int(lf):
                pytest_execute_params.append('--lf')
        # 判断是否清空已有测试结果
        if clr:
            if int(clr):
                pytest_execute_params.append('--clean-alluredir')
        pytest_execute_params.append(dir)
        # 构建孙进程
        process = multiprocessing.Process(target=pytest_main,args=(pytest_execute_params,))
        process.start()
        process.join()
        print('%s当前设备结束测试的desired_capabilities为:%s' % (DateTimeTool.getNowTime(),desired_capabilities))
    print('%s结束设备%s测试......'%(DateTimeTool.getNowTime(),device_info['device_desc']))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试',type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0',type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0',type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0',type=str)
    parser.add_argument('-tt', '--test_type', help='【必填】测试类型,phone、windows',type=str)
    parser.add_argument('-dif', '--devices_info_file', help='【必填】多设备并行信息文件，当--test_type为phone时，此选项需提供',type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    args=parser.parse_args()

    if not args.test_type:
        sys.exit('请指定测试类型,查看帮助:python run_app_ui_test.py --help')

    # 处理pytest文件
    deal_pytest_ini_file()

    # 初始化java依赖的libs
    java_maven_init()

    # 初始化httpserver
    http_server_init()

    # 初始化mitmproxy
    mitmproxy_init()

    keyword=args.keyword
    dir=args.dir
    markexpr=args.markexpr
    capture=args.capture
    reruns=args.reruns
    lf=args.lf
    clr=args.clr
    test_type=args.test_type.lower()
    devices_info_file=args.devices_info_file
    if test_type=='phone':
        if not devices_info_file:
            sys.exit('请指定多设备并行信息文件,查看帮助:python run_app_ui_test.py --help')
        print('%s开始初始化进程......'%DateTimeTool.getNowTime())
        p_pool = Custom_Pool(int(Read_APP_UI_Config().app_ui_config.max_device_pool))
        devices_info=Read_APP_UI_Devices_Info(devices_info_file).devices_info
        print('%s当前使用的配置文件为:%s'%(DateTimeTool.getNowTime(),devices_info_file))
        if os.path.exists('config/app_ui_tmp'):
            FileTool.truncateDir('config/app_ui_tmp/')
        else:
            os.mkdir('config/app_ui_tmp')
        for i in range(len(devices_info)):
            device_info=devices_info[i]
            FileTool.writeObjectIntoFile(device_info,'config/app_ui_tmp/'+str(i))
            p=p_pool.apply_async(start_app_device_test,(i,device_info,keyword,dir,markexpr,capture,reruns,lf,clr))
        p_pool.close()
        p_pool.join()
    else:
        # 执行pytest前的参数准备
        pytest_execute_params = ['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/app_ui/windows/report_data/']
        # 判断目录参数
        if not dir:
            dir = 'cases/app_ui/'
        # 判断关键字参数
        if keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(keyword)
        # 判断markexpr参数
        if args.markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(args.markexpr)
        # 判断是否输出日志
        if capture:
            if int(capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if reruns:
            if int(args.reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(reruns)
        # 判断是否只运行上一次失败的用例
        if lf:
            if int(lf):
                pytest_execute_params.append('--lf')
        # 判断是否清空已有测试结果
        if clr:
            if int(clr):
                pytest_execute_params.append('--clean-alluredir')
        pytest_execute_params.append(dir)
        exit_code = pytest.main(pytest_execute_params)

    # 当Python线程中执行jpype相关代码时会出现无法关闭jvm卡死的情况，故不进行主动关闭jvm，Python主进程结束自动关闭
    # print '关闭jvm......'
    # jpype.shutdownJVM()
