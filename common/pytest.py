# @Author  : yanchunhuo
# @Time    : 2020/1/15 14:08
import platform
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建配置文件的相对路径
config_path = os.path.join(current_dir, '../config', 'pytest.conf')
def deal_pytest_ini_file():
    """
    由于当前(2020/1/15)pytest运行指定的pytest.ini在Windows下编码有bug，故对不同环境进行处理
    """
    with open(config_path, 'r', encoding='utf-8') as pytest_f:
        content=pytest_f.read()
        if 'Windows'==platform.system():
            with open('config/pytest.ini','w+',encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)
                tmp_pytest_f.close()
        else:
            with open('config/pytest.ini','w+',encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)
                tmp_pytest_f.close()
        pytest_f.close()


