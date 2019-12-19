# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# 文件名 tee.py
# github https://github.com/yanchunhuo
from common.fileTool import FileTool
import os
import subprocess
import platform

def java_maven_init():
    print('开始java maven更新......')
    print('删除旧的maven依赖包......')
    FileTool.truncateDir('common/java/lib/java/libs')
    print('删除旧的maven依赖包完成......')
    maven_update_command = 'mvn -U -f "' + os.path.join(os.getcwd(),'config/java/pom.xml"') + ' dependency:copy-dependencies -DoutputDirectory="' + os.path.join(os.getcwd(), 'common/java/lib/java/libs"')
    output = subprocess.check_output(maven_update_command, shell=True, timeout=3600)
    if 'Windows' == platform.system():
        print(output.decode('cp936'))
    else:
        print(output.decode('utf-8'))
    print('完成java maven更新......')