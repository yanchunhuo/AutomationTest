#-*- coding:utf8 -*-
from base.read_app_ui_config import Read_APP_UI_Config
from common.httpclient.doRequest import DoRequest
from common.java.javaTools import JavaTool
from init.app_ui.android.android_init import android_init
from init.app_ui.chrome.chrome_init import chrome_init
from init.app_ui.ios.ios_init import ios_init
from init.app_ui.winwos.windows_init import windows_init
from init.java.java_maven_init import java_maven_init
import argparse
import jpype
import ujson
import pytest
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否')
    parser.add_argument('-r', '--reruns', help='失败重跑次数')
    args=parser.parse_args()

    print('开始初始化......')
    print('开始检测appium server是否可用......')
    try:
        doRquest=DoRequest(Read_APP_UI_Config().app_ui_config.appium_hub)

        httpResponseResult=doRquest.get('/status')
        result=ujson.loads(httpResponseResult.body)
        if result['status']==0:
            print('appium server状态为可用......')
        else:
            sys.exit('appium server状态为不可用')
    except:
        sys.exit('appium server状态为不可用')

    print('启动jvm......')
    jpype.startJVM(jpype.get_default_jvm_path(),"-ea","-Djava.class.path="+JavaTool.getAllJar())
    print('启动jvm成功')

    java_maven_init()

    print('初始化android基础数据......')
    android_init()
    print('初始化android基础数据完成......')

    print('初始化ios基础数据......')
    ios_init()
    print('初始化ios基础数据完成......')

    print('初始化windows基础数据......')
    windows_init()
    print('初始化windows基础数据完成......')

    print('初始化chrome基础数据......')
    chrome_init()
    print('初始化chrome基础数据完成......')

    print('初始化完成......')

    print('开始测试......')
    # 执行pytest前的参数准备
    pytest_execute_params=['-c', 'config/pytest.conf', '-v', '--alluredir', 'output/app_ui/']
    # 判断目录参数
    dir = 'cases/app_ui/'
    if args.dir:
        dir=args.dir
    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)
    # 判断是否输出日志
    if args.capture:
        pytest_execute_params.append('-s')
    # 判断是否失败重跑
    if args.reruns:
        pytest_execute_params.append('--reruns')
        pytest_execute_params.append(args.reruns)
    pytest_execute_params.append(dir)
    exit_code = pytest.main(pytest_execute_params)

    # 当Python线程中执行jpype相关代码时会出现无法关闭jvm卡死的情况，故不进行主动关闭jvm，Python主进程结束自动关闭
    # print '关闭jvm......'
    # jpype.shutdownJVM()

    print('结束测试......')
    sys.exit(exit_code)