![avatar](https://github.com/yanchunhuo/resources/blob/master/APIAutomationTest/report.png)

# [API自动化测试]()

# [概况]()
* 本项目由pytest、assertpy、requests、PyMySQL、allure、JPype1组成
    * pytest是python的一个单元测试框架,https://docs.pytest.org/en/latest/
    * assertpy是一个包含丰富的断言库，支持pytest,https://github.com/ActivisionGameScience/assertpy
    * requests是http请求框架,http://docs.python-requests.org/en/master/
    * PyMySQL用于操作MySQL数据库,https://github.com/PyMySQL/PyMySQL
    * allure用于生成测试报告,http://allure.qatools.ru/
    * JPype1用于执行java代码,https://github.com/jpype-project/jpype

# [使用]()
## 一、环境准备
### 1、安装python依赖模块
* pip3 install -r requirements.txt

### 2、安装allure
* 源安装
    * sudo apt-add-repository ppa:qameta/allure
    * sudo apt-get update 
    * sudo apt-get install allure
    * 其他安装方式：https://github.com/allure-framework/allure2
* 手动安装
    * 下载2.7.0版本:https://github.com/allure-framework/allure2/releases
    * 解压allure-2.7.0.zip
    * 加入系统环境变量:export PATH=/home/john/allure-2.7.0/bin:$PATH

### 3、安装openjdk8或jdk8
* sudo add-apt-repository ppa:openjdk-r/ppa
* sudo apt-get update
* sudo apt-get install openjdk-8-jdk

## 二、修改配置
* vim config/init.ini 配置需要初始化的项目
* vim config/projectName.ini 配置测试项目的信息

## 三、运行测试
* cd APIAutomationTest/
* python3 runTest.py --help
* python3 runTest.py 运行cases目录所有的用例
* python3 runTest.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 runTest.py -d dir     运行指定目录的用例，默认运行cases目录

## 四、生成测试报告
* cd APIAutomationTest/
* python3 generateReport.py -p 9080 
* 访问地址http://ip:9080
* 在使用Ubuntu进行报告生成时，请勿使用sudo权限，否则无法生成，allure不支持

# [项目结构]()
* base 基础请求类
* cases 测试用例目录
* common 公共模块
* config　配置文件
* init 初始化
* logs 日志目录
* output 测试结果输出目录 
* pojo 存放自定义类对象
* test_data 测试所需的测试数据目录
* runTest.py 测试运行脚本
* generateReport.py 报告生成脚本


# [编码规范]()
* 统一使用python 3.6
* 编码使用-\*- coding:utf8 -\*-,且不指定解释器
* 类/方法的注释均写在class/def下一行，并且用三个双引号形式注释
* 局部代码注释使用#号
* 所有的测试模块文件都以test_projectName_moduleName.py命名
* 所有的测试类都以Test开头，类中方法(用例)都以test_开头
* 每个测试项目都在cases目录里创建一个目录，且目录都包含有api、scenrarios两个目录
* case对应setup/teardown的fixture统一命名成fixture_[test_case_method_name]

# [pytest常用]()
* @pytest.mark.skip(reason='该功能已废弃')
* @pytest.mark.parametrize('key1,key2',[(key1_value1,key2_value2),(key1_value2,key2_value2)])
* @pytest.mark.usefixture('func_name')

# [注意点]()
* 运行pytest时指定的目录内应当有conftest.py，方能在其他模块中使用。@allure.step会影响fixture，故在脚本中不使用@allure.step

# [打赏]()
![avatar](https://github.com/yanchunhuo/resources/blob/master/Alipay.jpg)
