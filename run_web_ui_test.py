#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from base.read_mitmproxy_config import ReadMitmproxyConfig
from base.read_web_ui_config import ReadWebUiConfig
from common.date_time_tool import DateTimeTool
from common.file_tool import FileTool
from common.httpclient.do_request import DoRequest
from init.mitmproxy.mitmproxy_init import mitmproxy_init
from init.java.java_maven_init import java_maven_init
from init.web_ui.web_ui_init import web_ui_init
import argparse
import os
import pytest
import sys
import ujson

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-e','--env',help='指定测试环境,test:测试环境、release:正式环境')
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试',type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0',type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0',type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0',type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    parser.add_argument('-coce','--coce',help='收集用例失败是否继续执行,1:是、0:否,默认为0',type=str)
    args=parser.parse_args()

    mitmproxy_config=ReadMitmproxyConfig().mitmproxy_config
    web_ui_config=ReadWebUiConfig().web_ui_config
    print('%s开始初始化......'%DateTimeTool.get_now_time())
    print('%s开始检测selenium server是否可用......'%DateTimeTool.get_now_time())
    try:
        doRquest=DoRequest(web_ui_config['server']['selenium_hub'])
        doRquest.updateHeaders({"Content-Type": "application/json;charset=UTF-8"})
        httpResponseResult=doRquest.get('/status')
        result=ujson.loads(httpResponseResult.body)
        if result['value']['ready']:
            print('%sselenium server状态为可用......'%DateTimeTool.get_now_time())
        else:
            sys.exit('%sselenium server状态为不可用'%DateTimeTool.get_now_time())
    except:
        sys.exit('%sselenium server状态为不可用'%DateTimeTool.get_now_time())

    # 初始化java依赖的libs
    if web_ui_config['is_init_maven']:
        java_maven_init()
    # 初始化代理
    if mitmproxy_config['is_start_local_mitmproxy']:
        mitmproxy_init()
    # 存储要运行的环境信息
    if os.path.exists('config/tmp'):
        FileTool.truncate_dir('config/tmp/')
    else:
        os.mkdir('config/tmp')
    if args.env:
        env=args.env
        FileTool.write_object_into_file({'env':args.env},'config/tmp/env.json')

    print('%s初始化基础数据......'%DateTimeTool.get_now_time())
    web_ui_init()
    print('%s初始化基础数据完成......'%DateTimeTool.get_now_time())
    print('%s初始化完成......'%DateTimeTool.get_now_time())

    print('%s开始测试......'%DateTimeTool.get_now_time())
    exit_code = 0
    for current_browser in web_ui_config['browser']['test_browsers'].split('||'):
        print('%s开始%s浏览器测试......'%(DateTimeTool.get_now_time(),current_browser))
        # 由于pytest的并发插件xdist采用子进程形式，当前主进程的单例在子进程中会重新创建，所以将每次要测试的浏览器信息写入到文件中，
        # 保证子进程能够正确读取当前要测试的浏览器
        FileTool.replace_file_content('config/web_ui_config.yaml','\r\n','\n')
        FileTool.replace_file_content_with_lb_rb('config/web_ui_config.yaml',current_browser,'current_browser: ','\n')
        # 执行pytest前的参数准备
        pytest_execute_params=['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/web_ui/'+current_browser+'/report_data/','-n',str(web_ui_config['test']['test_workers']),'--dist','loadfile']
        # 判断目录参数
        dir = 'cases/web_ui/'
        if args.dir:
            dir=args.dir
        # 判断关键字参数
        if args.keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(args.keyword)
        # 判断markexpr参数
        if args.markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(args.markexpr)
        # 判断是否输出日志
        if args.capture:
            if int(args.capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if args.reruns:
            if int(args.reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(args.reruns)
        # 判断是否只运行上一次失败的用例
        if args.lf:
            if int(args.lf):
                pytest_execute_params.append('--lf')
        # 判断是否清空已有测试结果
        if args.clr:
            if int(args.clr):
                pytest_execute_params.append('--clean-alluredir')
        if args.coce:
            if int(args.coce):
                pytest_execute_params.append('--continue-on-collection-errors')
        pytest_execute_params.append(dir)
        tmp_exit_code = pytest.main(pytest_execute_params)
        if not tmp_exit_code==0:
            exit_code=tmp_exit_code
        print('%s结束%s浏览器测试......'%(DateTimeTool.get_now_time(),current_browser))
    
    
    print('%s清除未被关闭的浏览器......'%DateTimeTool.get_now_time())
    if os.path.exists('output/tmp/web_ui/driver_sessions_info'):
        with open('output/tmp/web_ui/driver_sessions_info','r',encoding='utf-8') as f:
            for line in f.readlines():
                line=line.strip()
                doRquest.delete('/session/%s'%line)
        FileTool.truncate_file('output/tmp/web_ui/driver_sessions_info')
    
    print('%s清除未被关闭的浏览器完成......'%DateTimeTool.get_now_time())

    print('%s结束测试......'%DateTimeTool.get_now_time())
