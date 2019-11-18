![avatar](https://github.com/yanchunhuo/resources/blob/master/APIAutomationTest/report.png)

# [自动化测试]()

# [概况]()
* 本项目支持接口自动化测试、app ui自动化测试、web ui自动化测试、性能测试
* 本项目由以下工具组成
    * pytest：python的一个单元测试框架,https://docs.pytest.org/en/latest/
    * pytest-xdist：pytest的一个插件,可多进程同时执行测试用例,https://github.com/pytest-dev/pytest-xdist
    * allure-pytest：用于生成测试报告,http://allure.qatools.ru/
    * assertpy：一个包含丰富的断言库，支持pytest,https://github.com/ActivisionGameScience/assertpy
    * requests：http请求框架,http://docs.python-requests.org/en/master/
    * Appium-Python-Client：移动端的自动化测试框架,https://github.com/appium/appium/tree/v1.9.1
    * selenium：web ui自动化测试框架,https://www.seleniumhq.org/
    * cx_Oracle：oracle操作库,https://cx-oracle.readthedocs.io/en/latest/index.html
    * JPype1：用于执行java代码,https://github.com/jpype-project/jpype
    * paramiko：ssh客户端,http://docs.paramiko.org/en/2.4/
    * Pillow：用于图片处理,https://pillow.readthedocs.io/en/latest/
    * PyMySQL：用于操作MySQL数据库,https://github.com/PyMySQL/PyMySQL
    * redis：redis客户端,https://pypi.org/project/redis/
    * tess4j：java的图片识别工具,http://tess4j.sourceforge.net/ 

# [使用]()
## 一、环境准备
### 1、脚本运行环境准备
#### 1.1、安装python依赖模块
* pip3 install -r requirements.txt

##### 1.1.1、安装xmind-sdk-python
* 地址:https://github.com/xmindltd/xmind-sdk-python

#### 1.2、安装allure
* 源安装
    * sudo apt-add-repository ppa:qameta/allure
    * sudo apt-get update 
    * sudo apt-get install allure
    * 其他安装方式：https://github.com/allure-framework/allure2
* 手动安装
    * 下载2.7.0版本:https://github.com/allure-framework/allure2/releases
    * 解压allure-2.7.0.zip
    * 加入系统环境变量:export PATH=/home/john/allure-2.7.0/bin:$PATH

#### 1.3、安装openjdk8或jdk8
* sudo add-apt-repository ppa:openjdk-r/ppa
* sudo apt-get update
* sudo apt-get install openjdk-8-jdk

#### 1.4、安装maven
* 完成maven的安装配置

#### 1.5、安装Oracle Instant Client
* linux
    * 安装libaio包
        * centos:yum install libaio
        * ubuntu:apt-get install libaio1
    * 配置Oracle Instant Client
        * 下载地址:http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html
        * 下载安装包instantclient-basic-linux.x64-18.3.0.0.0dbru.zip
        * 解压zip包,并配置/etc/profile
            * unzip instantclient-basic-linux.x64-18.3.0.0.0dbru.zip
            * export LD_LIBRARY_PATH=/home/john/oracle_instant_client/instantclient_18_3:$LD_LIBRARY_PATH
        * 中文编码设置
        
            ```python 
            import os
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
            ```
* Windows
    * 下载地址:http://www.oracle.com/technetwork/topics/winx64soft-089540.html
    * 下载安装包instantclient-basic-windows.x64-11.2.0.4.0.zip
    * 解压zip包,并配置环境变量
        * 系统环境变量加入D:\instantclient-basic-windows.x64-11.2.0.4.0\instantclient_11_2
        * 配置中文编码,环境变量创建NLS_LANG=SIMPLIFIED CHINESE_CHINA.UTF8  
    * 注意:如果使用64位,python和instantclient都需要使用64位

#### 1.6、图像识别字库准备
* 下载对应字库:https://github.com/tesseract-ocr/tessdata
* 将下载的字库放到common/java/lib/tess4j/tessdata/

### 2、selenium server运行环境准备
#### 2.1、安装jdk1.8,并配置环境变量
* export JAVA_HOME=/usr/lib/jvm/jdk8
* export JRE_HOME=${JAVA_HOME}/jre 
* export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
* export PATH=${JAVA_HOME}/bin:$PATH

#### 2.2、安装配置selenium
* 配置selenium server
    * 下载selenium-server-standalone-3.14.0.jar
    * 下载地址:http://selenium-release.storage.googleapis.com/index.html
    * 以管理员身份启动服务:java -jar selenium-server-standalone-3.14.0.jar -log selenium.log
* 下载浏览器驱动
    * 谷歌浏览器：https://chromedriver.storage.googleapis.com/index.html
    * 火狐浏览器：https://github.com/mozilla/geckodriver/
        * 驱动支持的浏览器版本：https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html
    * IE浏览器(建议使用32位,64位操作极慢)：http://selenium-release.storage.googleapis.com/index.html
    * 将驱动所在目录加入到selenium server服务器系统环境变量:export PATH=/home/john/selenium/:$PATH
* IE浏览器设置
    * 在Windows Vista、Windows7系统上的IE浏览器在IE7及以上版本中，需要设置四个区域的保护模式为一样，设置开启或者关闭都可以。
        * 工具-->Internet选项-->安全
    * IE10及以上版本增强保护模式需要关闭。
        * 工具-->Internet选项-->高级
    * 浏览器缩放级别必须设置为100%，以便本地鼠标事件可以设置为正确的坐标。
    * 针对IE11需要设置注册表以便于浏览器驱动与浏览器建立连接
        * Windows 64位：HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE
        * Windows 32位：HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE
        * 如果FEATRUE_BFCACHE项不存在，需要创建一个，然后在里面创建一个DWORD(32位)，命名为iexplore.exe，值为0
        * Windows 64位两个注册表建议都设置
    * IE8及以上版本设置支持inprivate模式，以便多开IE窗口时cookies能够独享
        * HKKY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main 下建一个名为TabProcGrowth的DWORD(32位)，值为0
    * 重启系统
    * 注:https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration

### 3、appium server运行环境准备
#### 3.1、安装jdk1.8,并配置环境变量
* export JAVA_HOME=/usr/lib/jvm/jdk8
* export JRE_HOME=${JAVA_HOME}/jre 
* export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
* export PATH=${JAVA_HOME}/bin:$PATH

#### 3.2、安装配置appium server
* 安装appium desktop server
    * 下载appium-desktop-setup-1.8.2.exe
    * 下载地址:https://github.com/appium/appium-desktop/releases
    * 以管理员身份启动服务

* Android环境准备
    * 安装java(JDK),并配置JAVA_HOME=/usr/lib/jvm/jdk8
    * 安装Android SDK,并配置ANDROID_HOME="/usr/local/adt/sdk"
    * 使用SDK manager安装需要进行自动化的Android API版本

* 手机chrome环境准备
    * 确保手机已安装chrome浏览器
    * 下载chrome浏览器驱动：https://chromedriver.storage.googleapis.com/index.html
    * 驱动支持的手机浏览器版本：https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/web/chromedriver.md
    * 在appium desktop上设置驱动的路径

* Windows环境准备
    * 支持Windows10及以上版本
    * 设置Windows处于开发者模式
    * 下载WinAppDriver并安装(V1.1版本),https://github.com/Microsoft/WinAppDriver/releases
    * \[可选\]下载安装WindowsSDK,在Windows Kits\10\bin\10.0.17763.0\x64内包含有inspect.exe用于定位Windows程序的元素信息

* 其他更多配置：https://github.com/appium/appium/tree/v1.9.1/docs/en/drivers

## 二、修改配置
* vim config/app_ui_config.conf 配置app ui自动化的测试信息
* vim config/web_ui_config.conf 配置web ui自动化的测试信息
* vim config/projectName/projectName.conf 配置测试项目的信息

## 三、运行测试
### 1、API测试
* cd AutomationTest/
* python3 -u run_api_test.py --help
* python3 -u run_api_test.py 运行cases目录所有的用例
* python3 -u run_api_test.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_api_test.py -d dir     运行指定目录的用例，默认运行cases目录

### 2、web ui测试
* cd AutomationTest/
* python3 -u run_web_ui_test.py --help
* python3 -u run_web_ui_test.py 运行cases目录所有的用例
* python3 -u run_web_ui_test.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_web_ui_test.py -d dir     运行指定目录的用例，默认运行cases目录

### 3、app ui测试
* cd AutomationTest/
* python3 -u run_app_ui_test.py --help
* python3 -u run_app_ui_test.py 运行cases目录所有的用例
* python3 -u run_app_ui_test.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_app_ui_test.py -d dir     运行指定目录的用例，默认运行cases目录

## 四、生成测试报告
### 1、API测试
* cd AutomationTest/
* python3 -u generate_api_test_report.py -p 9080 
* 访问地址http://ip:9080
* 在使用Ubuntu进行报告生成时，请勿使用sudo权限，否则无法生成，allure不支持

### 2、web ui测试
* cd AutomationTest/
* python3 -u generateReport_web_ui_test_report.py -ieport 9081 -chromeport 9082 -firefoxport 9083
* 访问地址http://ip:908[1-3]
* 在使用Ubuntu进行报告生成时，请勿使用sudo权限，否则无法生成，allure不支持

### 3、app ui测试
* cd AutomationTest/
* python3 -u generateReport_app_ui_test_report.py -p 9084
* 访问地址http://ip:9084

### 注：在使用Ubuntu进行报告生成时，请勿使用sudo权限，否则无法生成，allure不支持

## 五、项目说明
### 1、API测试
* 项目
    * demoProject
        * 例子项目
        
### 2、web ui测试
* 元素的显式等待时间默认为30s
* 封装的显式等待类型支持:page_objects/web_ui/wait_type.py
* 封装的定位类型支持:page_objects/web_ui/locator_type.py
* 默认使用4个worker进行并行测试
* 文件下载处理暂不支持ie浏览器
* 无头浏览器暂不支持ie浏览器
* 项目
    * demoProject
        * 例子项目
        
### 3、app ui测试
* 元素的显式等待时间默认为30s
* 封装的显式等待类型支持:page_objects/app_ui/wait_type.py
* 封装的定位类型支持:page_objects/app_ui/locator_type.py
* 项目
    * demoProject
        * 例子项目

# [项目结构]()
* base 基础请求类
* cases 测试用例目录
* common 公共模块
* common_projects 每个项目的公共模块
* config　配置文件
* init 初始化
* logs 日志目录
* output 测试结果输出目录 
* packages app ui测试的安装包
* pojo 存放自定义类对象
* test_data 测试所需的测试数据目录
* run_api_test.py 运行api测试脚本
* run_web_ui_test.py 运行web ui测试脚本
* run_app_ui_test.py 运行app ui测试脚本
* generate_api_test_report.py 生成api测试报告
* generateReport_web_ui_test_report.py 生成web ui测试报告
* generateReport_app_ui_test_report.py 生成app ui测试报告

# [编码规范]()
* 统一使用python 3.6
* 编码使用-\*- coding:utf8 -\*-,且不指定解释器
* 类/方法的注释均写在class/def下一行，并且用三个双引号形式注释
* 局部代码注释使用#号
* 所有中文都直接使用字符串，不转换成Unicode，即不是用【u'中文'】编写
* 所有的测试模块文件都以test_projectName_moduleName.py命名
* 所有的测试类都以Test开头，类中方法(用例)都以test_开头
* 每个测试项目都在cases目录里创建一个目录，且目录都包含有api、scenrarios两个目录
* case对应setup/teardown的fixture统一命名成fixture_[test_case_method_name]
* 每一个模块中测试用例如果有顺序要求【主要针对ui自动化测试】，则自上而下排序，pytest在单个模块里会自上而下按顺序执行

# [pytest常用]()
* @pytest.mark.skip(reason='该功能已废弃')
* @pytest.mark.parametrize('key1,key2',[(key1_value1,key2_value2),(key1_value2,key2_value2)])
* @pytest.mark.usefixture('func_name')

# [注意点]()
* 运行pytest时指定的目录内应当有conftest.py，方能在其他模块中使用。@allure.step会影响fixture，故在脚本中不使用@allure.step
* web ui测试
    * 统一使用Firefox浏览器进行元素定位
    * 能用id、name、link(不常变化的链接)定位的，不使用css定位，能使用css定位，不使用xpath定位
    * 项目使用并发运行，故编写测试用例时，应该避免模块与模块直接的用例会相互影响测试结果
* app ui测试
    * 能用id、name、link(不常变化的链接)定位的，不使用css定位，能使用css定位，不使用xpath定位
    * 如需要上传文件到手机或者从手机下载文件，请确保有手机对应目录的读写权限
    * 视频录制统一对单个单个case进行，保证录制时间不超过3分钟，且录制文件不要过大，否则会引起手机内存无法存储视频
            * 确认手机是否能进行视频录制执行命令adb shell screenrecord /sdcard/test.mp4，能正常执行即可
    * 设备屏幕坐标系原点都在最左上角，往右x轴递增，往下y轴递增

# [打赏]()
![avatar](https://github.com/yanchunhuo/resources/blob/master/Alipay.jpg)
