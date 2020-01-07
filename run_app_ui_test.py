#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.read_app_ui_config import Read_APP_UI_Config
from base.read_app_ui_devices_info import Read_APP_UI_Devices_Info
from common.httpclient.doRequest import DoRequest
from common.fileTool import FileTool
from init.java.java_maven_init import java_maven_init
import argparse
import multiprocessing
import os
import pytest
import sys
import ujson

def start_app_device_test(index,device_info,keyword,dir,markexpr,capture,reruns,lf):
    for path, dirs, files in os.walk('config/app_ui_tmp'):
        for file in files:
            if(int(file)==index):
                os.rename(os.path.join(path,file),os.path.join(path,str(os.getpid())))

    print('开始检测appium server是否可用......')
    try:
        doRquest = DoRequest('http://'+device_info['server_ip']+':%s/wd/hub'%device_info['server_port'].strip())
        httpResponseResult = doRquest.get('/status')
        result = ujson.loads(httpResponseResult.body)
        if result['status'] == 0:
            print('appium server状态为可用......')
        else:
            sys.exit('appium server状态为不可用')
    except:
        sys.exit('appium server状态为不可用')

    print('开始设备'+device_info['device_desc']+'测试......')
    # 执行pytest前的参数准备
    pytest_execute_params = ['-c', 'config/pytest.conf', '-v', '--alluredir', 'output/app_ui/'+device_info['device_desc']]
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
    pytest_execute_params.append(dir)
    exit_code = pytest.main(pytest_execute_params)
    print('结束设备'+device_info['device_desc']+'测试......')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试')
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0')
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0')
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0')
    parser.add_argument('-tt', '--test_type', help='【必填】测试类型,phone、windows')
    parser.add_argument('-dif', '--devices_info_file', help='多设备并行信息文件，当--test_type为android、ios、chrome时，此选项需提供')
    args=parser.parse_args()

    java_maven_init()

    if not args.test_type:
        sys.exit('请指定测试类型,查看帮助:python run_app_ui_test.py --help')
    keyword=args.keyword
    dir=args.dir
    markexpr=args.markexpr
    capture=args.capture
    reruns=args.reruns
    lf=args.lf
    test_type=args.test_type.lower()
    devices_info_file=args.devices_info_file
    if test_type=='phone':
        if not devices_info_file:
            sys.exit('请指定多设备并行信息文件,查看帮助:python run_app_ui_test.py --help')
        # 初始化进程池
        p_pool = multiprocessing.Pool(int(Read_APP_UI_Config().app_ui_config.max_device_pool))
        devices_info=Read_APP_UI_Devices_Info(devices_info_file).devices_info
        if os.path.exists('config/app_ui_tmp'):
            FileTool.truncateDir('config/app_ui_tmp/')
        else:
            os.mkdir('config/app_ui_tmp')
        for i in range(len(devices_info)):
            device_info=devices_info[i]
            FileTool.writeObjectIntoFile(device_info,'config/app_ui_tmp/'+str(i))
            p=p_pool.apply_async(start_app_device_test,(i,device_info,keyword,dir,markexpr,capture,reruns,lf))
        p_pool.close()
        p_pool.join()
    else:
        # 执行pytest前的参数准备
        pytest_execute_params = ['-c', 'config/pytest.conf', '-v', '--alluredir', 'output/app_ui/windows']
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
        pytest_execute_params.append(dir)
        exit_code = pytest.main(pytest_execute_params)
        sys.exit(exit_code)

    # 当Python线程中执行jpype相关代码时会出现无法关闭jvm卡死的情况，故不进行主动关闭jvm，Python主进程结束自动关闭
    # print '关闭jvm......'
    # jpype.shutdownJVM()
