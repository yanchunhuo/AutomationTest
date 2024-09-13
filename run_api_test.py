#
# run_api_test.py
# @author yanchunhuo
# @description 
# @github https://github.com/yanchunhuo
# @created 2021-04-13T10:59:18.120Z+08:00
# @last-modified 2024-09-13T14:50:26.965Z+08:00
#
from base.read_api_config import ReadAPIConfig
from common.date_time_tool import DateTimeTool
from common.file_tool import FileTool
from init.api.api_init import api_init
from init.java.java_maven_init import java_maven_init
import argparse
import os
import pytest

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    parser.add_argument('-coce','--coce',help='收集用例失败是否继续执行,1:是、0:否,默认为0',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-e','--env',help='指定测试环境,test:测试环境、release:正式环境')
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0',type=str)
    parser.add_argument('-m','--markexpr',help='只运行符合给定的mark表达式的测试',type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0',type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0',type=str)
    
    args=parser.parse_args()

    # 初始化java依赖的libs
    if ReadAPIConfig().config['is_init_maven']:
        java_maven_init()

    # 初始化
    print('%s开始初始化......'%DateTimeTool.get_now_time())
    api_init()
    print('%s初始化完成......'%DateTimeTool.get_now_time())

    # 执行pytest前的参数准备
    pytest_execute_params=['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/api/report_data/']
    # 判断目录参数
    dir = 'cases/api/'
    # 判断是否清空已有测试结果
    if args.clr:
        if int(args.clr):
            pytest_execute_params.append('--clean-alluredir')
    if args.coce:
        if int(args.coce):
            pytest_execute_params.append('--continue-on-collection-errors')
    if args.dir:
        dir=args.dir
    # 存储要运行的环境信息
    if os.path.exists('config/tmp'):
        FileTool.truncate_dir('config/tmp/')
    else:
        os.mkdir('config/tmp')
    if args.env:
        env=args.env
        FileTool.write_object_into_file({'env':args.env},'config/tmp/env.json')
    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)
    # 判断是否只运行上一次失败的用例
    if args.lf:
        if int(args.lf):
            pytest_execute_params.append('--lf')
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
    
    pytest_execute_params.append(dir)

    print('%s开始测试......'%DateTimeTool.get_now_time())
    exit_code=pytest.main(pytest_execute_params)
    # 存储运行结果信息
    if os.path.exists('output/api/tmp'):
        FileTool.truncate_dir('output/api/tmp')
    else:
        os.mkdir('output/api/tmp')
    FileTool.write_object_into_file({'result':exit_code.numerator},'output/api/tmp/result.json')