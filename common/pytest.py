# @Author  : yanchunhuo
# @Time    : 2020/1/15 14:08
import platform

def deal_pytest_ini_file():
    """
    由于当前(2020/1/15)pytest运行指定的pytest.ini在Windows下编码有bug，故对不同环境进行处理
    """
    with open('config/pytest.conf','r',encoding='utf-8') as pytest_f:
        content=pytest_f.read()
        if 'Windows'==platform.system():
            with open('config/pytest.ini','w+',encoding='gbk') as tmp_pytest_f:
                tmp_pytest_f.write(content)
                tmp_pytest_f.close()
        else:
            with open('config/pytest.ini','w+',encoding='utf-8') as tmp_pytest_f:
                tmp_pytest_f.write(content)
                tmp_pytest_f.close()
        pytest_f.close()


