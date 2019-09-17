#-*- coding:utf8 -*-
from init.init import init
import argparse
import pytest
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    args=parser.parse_args()

    # 初始化
    print('开始初始化......')
    init()
    print('初始化完成......')

    # 执行pytest前的参数准备
    pytest_execute_params=['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/','--clean-alluredir']
    # 判断目录参数
    dir = 'cases'
    if args.dir:
        dir=args.dir
    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)

    pytest_execute_params.append(dir)

    print('开始测试......')
    exit_code=pytest.main(pytest_execute_params)
    sys.exit(exit_code)