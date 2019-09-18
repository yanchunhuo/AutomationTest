#-*- coding:utf8 -*-
from base.read_web_ui_config import Read_WEB_UI_Config
from common.fileTool import FileTool
from common.httpclient.doRequest import DoRequest
from init.web_ui.web_ui_init import init
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.command import Command
import argparse
import json
import pytest
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    args=parser.parse_args()

    print('开始初始化......')
    print('开始检测selenium server是否可用......')
    try:
        doRquest=DoRequest(Read_WEB_UI_Config().web_ui_config.selenium_hub)
        httpResponseResult=doRquest.get('/status')
        result=json.loads(httpResponseResult.body)
        if result['status']==0:
            print('selenium server状态为可用......')
        else:
            sys.exit('selenium server状态为不可用')
    except:
        sys.exit('selenium server状态为不可用')

    print('初始化基础数据......')
    init()
    print('初始化基础数据完成......')
    print('初始化完成......')

    print('开始测试......')
    exit_code = 0
    for current_browser in Read_WEB_UI_Config().web_ui_config.test_browsers:
        print('开始'+current_browser+'浏览器测试......')
        # 由于pytest的并发插件xdist采用子进程形式，当前主进程的单例在子进程中会重新创建，所以将每次要测试的浏览器信息写入到文件中，
        # 保证子进程能够正确读取当前要测试的浏览器
        FileTool.replaceFileContent('config/config.conf','\r\n','\n')
        FileTool.replaceFileContentWithLBRB('config/config.conf','='+current_browser,'current_browser','\n')
        # 执行pytest前的参数准备
        pytest_execute_params=['-c', 'config/pytest.conf', '-v', '--alluredir', 'output/web_ui/'+current_browser+'/','--clean-alluredir','-n',Read_WEB_UI_Config().web_ui_config.test_workers,'--dist','loadfile']
        # 判断目录参数
        dir = 'cases/web_ui/'
        if args.dir:
            dir=args.dir
        # 判断关键字参数
        if args.keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(args.keyword)
        pytest_execute_params.append(dir)
        tmp_exit_code = pytest.main(pytest_execute_params)
        if not tmp_exit_code==0:
            exit_code=tmp_exit_code
        print('结束' + current_browser + '浏览器测试......')
    
    print('清除未被关闭的浏览器......')
    try:
        conn=RemoteConnection(Read_WEB_UI_Config().web_ui_config.selenium_hub,True)
        sessions=conn.execute(Command.GET_ALL_SESSIONS,None)
        sessions=sessions['value']
        for session in sessions:
            session_id=session['id']
            conn.execute(Command.QUIT,{'sessionId':session_id})
    except Exception as e:
        print('清除未关闭浏览器异常:\r\n'+e.args.__str__())
    print('清除未被关闭的浏览器完成......')

    print('结束测试......')
    sys.exit(exit_code)
