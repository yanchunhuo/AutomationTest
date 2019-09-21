from common.fileTool import FileTool
import os
import subprocess
import sys

def tess4j_maven_init():
    print('开始tess4j maven更新......')
    print('删除旧的maven依赖包......')
    FileTool.truncateDir('common/java/lib/tess4j/libs')
    print('删除旧的maven依赖包完成......')
    maven_update_command = 'mvn -U -f ' + os.path.join(os.getcwd(),'config/tess4j/pom.xml') + ' dependency:copy-dependencies -DoutputDirectory=' + os.path.join(os.getcwd(), 'common/java/lib/tess4j/libs')
    try:
        output = subprocess.check_output(maven_update_command, shell=True, timeout=3600)
        print(output.decode('utf-8'))
    except:
        sys.exit('tess4j maven更新失败......')
    print('完成tess4j maven更新......')