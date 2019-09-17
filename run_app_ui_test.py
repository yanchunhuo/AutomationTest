#-*- coding:utf8 -*-
from base.readConfig import ReadConfig
from common.httpclient.doRequest import DoRequest
from common.java.javaTool import JavaTool
from init.android.android_init import android_init
from init.chrome.chrome_init import chrome_init
from init.ios.ios_init import ios_init
from init.winwos.windows_init import windows_init
import argparse
import jpype
import json
import pytest
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    args=parser.parse_args()

    print('开始初始化......')
    print('开始检测appium server是否可用......')
    try:
        doRquest=DoRequest(ReadConfig().config.appium_hub)

        httpResponseResult=doRquest.get('/status')
        result=json.loads(httpResponseResult.body)
        if result['status']==0:
            print('appium server状态为可用......')
        else:
            sys.exit('appium server状态为不可用')
    except:
        sys.exit('appium server状态为不可用')

    print('启动jvm......')
    jpype.startJVM(jpype.get_default_jvm_path(),"-ea","-Djava.class.path="+JavaTool.getAllJar())
    print('启动jvm成功')

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
    pytest_execute_params=['-c', 'config/pytest.conf', '-v', '--alluredir', 'output/','--clean-alluredir']
    # 判断目录参数
    dir = 'cases/'
    if args.dir:
        dir=args.dir
    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)
    pytest_execute_params.append(dir)
    exit_code = pytest.main(pytest_execute_params)

    # 当Python线程中执行jpype相关代码时会出现无法关闭jvm卡死的情况，故不进行主动关闭jvm，Python主进程结束自动关闭
    # print '关闭jvm......'
    # jpype.shutdownJVM()

    print('结束测试......')
    sys.exit(exit_code)