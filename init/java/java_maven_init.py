# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from common.dateTimeTool import DateTimeTool
from common.fileTool import FileTool
import os
import subprocess
import platform

def java_maven_init():
    print('%s开始java maven更新......'%DateTimeTool.getNowTime())
    print('%s删除旧的maven依赖包......'%DateTimeTool.getNowTime())
    FileTool.truncateDir('common/java/lib/java/libs')
    print('%s删除旧的maven依赖包完成......'%DateTimeTool.getNowTime())
    maven_update_command = 'mvn -U -f "' + os.path.join(os.getcwd(),'config/java/pom.xml"') + ' dependency:copy-dependencies -DoutputDirectory="' + os.path.join(os.getcwd(), 'common/java/lib/java/libs"')
    output = subprocess.check_output(maven_update_command, shell=True, timeout=3600)
    if 'Windows' == platform.system():
        print(output.decode('cp936'))
    else:
        print(output.decode('utf-8'))
    print('%s完成java maven更新......'%DateTimeTool.getNowTime())