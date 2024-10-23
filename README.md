![avatar](https://github.com/yanchunhuo/resources/blob/master/APIAutomationTest/report.png)

# [自动化测试]()

# [概况]()
* 本项目支持接口自动化测试、app ui自动化测试、web ui自动化测试、性能测试
* 本项目由以下工具组成
    * allure-pytest：pytest的一个插件，用于生成测试报告，http://allure.qatools.ru/
    * Appium：移动端的自动化测试框架，https://github.com/appium/appium
    * beautifulsoup4：页面解析库，https://www.crummy.com/software/BeautifulSoup/
    * JPype1：用于执行java代码，https://github.com/jpype-project/jpype
    * Js2Py：用于执行js代码，https://github.com/PiotrDabkowski/Js2Py
    * lxml：用于beautifulsoup4页面解析引擎，https://lxml.de/
    * mitmproxy：用于HTTP/1、HTTP/2和WebSockets的交互式、支持SSL/TLS的拦截代理，https://mitmproxy.org/
    * paramiko：ssh客户端，https://github.com/paramiko/paramiko
    * pycryptodome：加密库，https://github.com/Legrandin/pycryptodome/
    * PyHamcrest：一个匹配器对象的框架，用于断言，https://github.com/hamcrest/PyHamcrest
    * PyMySQL：用于操作MySQL数据库，https://github.com/PyMySQL/PyMySQL
    * pytest：python的一个单元测试框架,https://docs.pytest.org/en/latest/
    * pytest-rerunfailures：pytest的一个插件，用于重跑测试用例，https://github.com/pytest-dev/pytest-rerunfailures
    * pytest-xdist：pytest的一个插件,可多进程同时执行测试用例，https://github.com/pytest-dev/pytest-xdist
    * python-binary-memcached：用于操作memcached，https://github.com/jaysonsantos/python-binary-memcached
    * PyJWT：JWT的实现，https://github.com/jpadilla/pyjwt
    * redis：redis客户端，https://github.com/redis/redis-py
    * requests：http请求框架，http://docs.python-requests.org/en/master/
    * scikit-image：图形处理，https://github.com/scikit-image/scikit-image
    * selenium：web ui自动化测试框架,https://www.seleniumhq.org/
    * sqlacodegen：用于根据数据库表结构生成python对象，https://github.com/agronholm/sqlacodegen
    * SQLAlchemy：SQL工具包及对象关系映射（ORM）工具，https://github.com/sqlalchemy/sqlalchemy
    * ujson：一个用纯C编写的超快JSON编码器和解码器
    * tess4j：java的图片识别工具，https://github.com/nguyenq/tess4j/
* 当前仅支持Python3.7、Python3.8、Python3.9
    * 建议安装：V3.9.13版本
* 项目如需执行java代码(即使用jpype1)，则项目目录所在的路径不可包含中文
* dubbo当前支持V2.6.0

# [使用]()
## 一、环境准备
### 1、脚本运行环境准备
#### 1.1、安装系统依赖
* Linux-Ubuntu：
    * sudo apt-get install g++ python-dev python3-dev
        * 说明：g++、python-dev、python3-dev是Jpype1依赖所需
* Linux-CentOS：
    * yum install gcc-c++ python-devel python3-devel
        * 说明：gcc-c++、python-devel、python3-devel是Jpype1依赖所需
* Windows：
    * 安装Microsoft Visual C++ 2015-2022 Redistributable
        * 下载页面：https://learn.microsoft.com/en-GB/cpp/windows/latest-supported-vc-redist?view=msvc-170
            * 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe
        * 说明：Microsoft Visual C++ 2015-2022 Redistributable是mitmproxy依赖所需

#### 1.2、安装jdk11
* 安装jdk11，并配置JAVA_HOME系统环境变量

#### 1.3、安装maven
* 完成maven的安装配置，建议更换国内仓库，提高包下载速度
* 配置jar包依赖配置文件为：config/java/pom.xml

#### 1.4、安装python依赖模块
* python -m pip install --upgrade pip3
* pip3 install -r requirements.txt

#### 1.5、安装allure
* 源安装
    * sudo apt-add-repository ppa:qameta/allure
    * sudo apt-get update 
    * sudo apt-get install allure
    * 其他安装方式：https://github.com/allure-framework/allure2
* 手动安装
    * 下载2.20.1版本:https://github.com/allure-framework/allure2/releases
    * 解压allure-2.20.1.zip
    * 加入系统环境变量:export PATH=/home/john/allure-2.20.1/bin:$PATH

### 2、selenium server运行环境准备
#### 2.1、安装jdk11
* 安装jdk11，并配置JAVA_HOME系统环境变量

#### 2.2、安装配置selenium
* 配置selenium server
    * 下载selenium-server-4.6.0.jar
    * 下载地址：https://github.com/SeleniumHQ/selenium/releases
    * 以管理员身份启动服务:java -jar selenium-server-4.6.0.jar standalone --log selenium.log
        * 其他可选项说明：java -jar selenium-server-4.6.0.jar standalone --help
* 下载浏览器驱动
    * 谷歌浏览器：https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
        * 驱动支持的最低浏览器版本：https://raw.githubusercontent.com/appium/appium-chromedriver/master/config/mapping.json
        * 其他下载地址（115之前版本）：https://registry.npmmirror.com/binary.html?path=chromedriver
        * 其他下载地址（115之后版本），直接替换浏览器版本号进行下载：https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/win64/chromedriver-win64.zip
    * 火狐浏览器：https://github.com/mozilla/geckodriver/
        * 驱动支持的浏览器版本：https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/Support.html
    * Edge浏览器：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    * Safari浏览器：操作系统内置，无需下载配置。启用在命令行执行：safaridriver --enable
    * 将驱动所在目录加入到selenium server服务器系统环境变量:export PATH=/home/john/selenium/:$PATH
    * 注意：请勿重命名驱动文件名

===========================================================
* Linux-Ubuntu:
    * apt-get install libpq-dev python3-dev 【用于psycopg2-binary所需依赖】
    * apt-get install g++ libgraphicsmagick++1-dev libboost-python-dev 【用于pgmagick所需依赖】
    * apt-get install python-pgmagick 【pgmagick所需依赖】
* Linux-CentOS:
    * yum install python3-devel postgresql-devel 【用于psycopg2-binary所需依赖】
    * yum install GraphicsMagick-c++-devel boost boost-devel【用于pgmagick所需依赖】
* Windows:
    * 安装Microsoft Visual C++ 2019 Redistributable，下载地址：https://visualstudio.microsoft.com/zh-hans/downloads/ 【jpype1、图像识别字库所需依赖】

#### 1.2、安装python依赖模块
* pip3 install -r requirements.txt
* 安装pgmagick
    * Linux:
        * pip3 install pgmagick==0.7.6
    * Windows:
        * 下载安装对应版本：https://www.lfd.uci.edu/~gohlke/pythonlibs/#pgmagick
* 安装xmind-sdk-python
    * 下载地址:https://github.com/xmindltd/xmind-sdk-python

#### 1.3、安装allure
* 源安装
    * sudo apt-add-repository ppa:qameta/allure
    * sudo apt-get update 
    * sudo apt-get install allure
    * 其他安装方式：https://github.com/allure-framework/allure2
* 手动安装
    * 下载2.7.0版本:https://github.com/allure-framework/allure2/releases
    * 解压allure-2.7.0.zip
    * 加入系统环境变量:export PATH=/home/john/allure-2.7.0/bin:$PATH

#### 1.4、安装openjdk8或jdk8
* sudo add-apt-repository ppa:openjdk-r/ppa
* sudo apt-get update
* sudo apt-get install openjdk-8-jdk

#### 1.5、安装maven
* 完成maven的安装配置

#### 1.7、图像识别字库准备
* 下载对应字库:https://github.com/tesseract-ocr/tessdata
* 将下载的字库放到common/java/lib/tess4j/tessdata/
* Linux
    * 安装依赖
        * Linux-Ubuntu:sudo apt install pkg-config aclocal libtool automake libleptonica-dev
        * Linux-CentOS:yum install autoconf automake libtool libjpeg-devel libpng-devel libtiff-devel zlib-devel
    * 安装leptonica，下载leptonica-1.78.0.tar.gz，下载地址：https://github.com/DanBloomberg/leptonica/releases
        * 安装步骤同tesseract-ocr的安装
        * 修改/etc/profile添加如下内容，然后source
        ```
        export LD_LIBRARY_PATH=$LD_LIBRARY_PAYT:/usr/local/lib
        export LIBLEPT_HEADERSDIR=/usr/local/include
        export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
        ```
    * 安装tesseract-ocr，下载tesseract-4.1.1.tar.gz，下载地址：https://github.com/tesseract-ocr/tesseract/releases
        * ./autogen.sh
        * ./configure
        * sudo make
        * sudo make install
        * sudo ldconfig
* Windows
    * 安装Microsoft Visual C++ 2019 Redistributable，下载地址：https://visualstudio.microsoft.com/zh-hans/downloads/

### 2、selenium server运行环境准备
#### 2.1、安装jdk1.8,并配置环境变量
* export JAVA_HOME=/usr/lib/jvm/jdk8
* export JRE_HOME=${JAVA_HOME}/jre 
* export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
* export PATH=${JAVA_HOME}/bin:$PATH

#### 2.2、安装配置selenium
* 配置selenium server
    * 下载selenium-server-standalone-3.141.0.jar
    * 下载地址:http://selenium-release.storage.googleapis.com/index.html
    * 以管理员身份启动服务:java -jar selenium-server-standalone-3.141.0.jar -log selenium.log
        * 其他可选项说明：java -jar selenium-server-4.5.3.jar standalone --help
* 下载浏览器驱动
    * 谷歌浏览器：https://chromedriver.storage.googleapis.com/index.html
        * 驱动支持的最低浏览器版本：https://raw.githubusercontent.com/appium/appium-chromedriver/master/config/mapping.json
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
    * 下载Appium-windows-1.15.1.exe
    * 下载地址:https://github.com/appium/appium-desktop/releases
    * 以管理员身份启动服务

* Android环境准备
    * 安装java(JDK),并配置JAVA_HOME=/usr/lib/jvm/jdk8
    * 安装Android SDK,并配置ANDROID_HOME="/usr/local/adt/sdk"
    * 使用SDK manager安装需要进行自动化的Android API版本
    
* IOS环境准备
    * 由于测试IOS真实设备没办法直接操作web view，需要通过usb，实现通过usb创建连接需要安装ios-webkit-debug-proxy
    * 下载安装地址：https://github.com/google/ios-webkit-debug-proxy/tree/v1.8.5

* 手机chrome环境准备
    * 确保手机已安装chrome浏览器
    * 下载chrome浏览器驱动：https://chromedriver.storage.googleapis.com/index.html
    * 驱动支持的最低浏览器版本：https://raw.githubusercontent.com/appium/appium-chromedriver/master/config/mapping.json
    * 在appium desktop上设置驱动的路径

* 混合应用环境准备
    * 方法一：安装TBS Studio工具查看webview内核版本：https://x5.tencent.com/tbs/guide/debug/season1.html
    * 方法二：打开地址（该地址在uc开发工具中可查到）查看webview内核版本：https://liulanmi.com/labs/core.html
    * 下载webview内核对应的chromedriver版本：https://chromedriver.storage.googleapis.com/index.html
    * 配置文件进行驱动路径的配置
    * 注：webview需要开启debug模式

* Windows环境准备
    * 支持Windows10及以上版本
    * 设置Windows处于开发者模式
    * 下载WinAppDriver并安装(V1.1版本),https://github.com/Microsoft/WinAppDriver/releases
    * \[可选\]下载安装WindowsSDK,在Windows Kits\10\bin\10.0.17763.0\x64内包含有inspect.exe用于定位Windows程序的元素信息

* 其他更多配置：https://github.com/appium/appium/tree/v1.15.1/docs/en/drivers

## 二、修改配置
* vim config/app_ui_config.conf 配置app ui自动化的测试信息
* vim config/web_ui_config.yaml 配置web ui自动化的测试信息
* vim config/projectName/projectName.conf 配置测试项目的信息
* 修改性能测试负载机的系统最大打开文件数,避免并发用户数大于最大打开文件数

## 三、运行测试
### 1、API测试
* cd AutomationTest/
* python3 -u run_api_test.py --help
* python3 -u run_api_test.py 运行cases/api/目录所有的用例
* python3 -u run_api_test.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_api_test.py -d dir     运行指定目录的用例，默认运行cases/api/目录
* python3 -u run_api_test.py -m mark    运行指定标记的用例

### 2、web ui测试
* cd AutomationTest/
* python3 -u run_web_ui_test.py --help
* python3 -u run_web_ui_test.py 运行cases/web_ui/目录所有的用例
* python3 -u run_web_ui_test.py -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_web_ui_test.py -d dir     运行指定目录的用例，默认运行cases/web_ui/目录
* python3 -u run_web_ui_test.py -m mark    运行指定标记的用例

### 3、app ui测试
* cd AutomationTest/
* python3 -u run_app_ui_test.py --help
* python3 -u run_app_ui_test.py 运行cases/app_ui/目录所有的用例
* python3 -u run_app_ui_test.py -tt phone -k keyword 运行匹配关键字的用例，会匹配文件名、类名、方法名
* python3 -u run_app_ui_test.py -tt phone -d dir     运行指定目录的用例，默认运行cases/app_ui/目录
* python3 -u run_app_ui_test.py -m mark              运行指定标记的用例

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
* python3 -u generateReport_app_ui_test_report.py -sp 9084
* 访问地址http://ip:9084

### 注：在使用Ubuntu进行报告生成时，请勿使用sudo权限，否则无法生成，allure不支持

## 五、项目说明
### 1、API测试
* 项目
    * demoProject 例子项目
        
### 2、web ui测试
* 元素的显式等待时间默认为30s
* 封装的显式等待类型支持:page_objects/web_ui/wait_type.py
* 封装的定位类型支持:page_objects/web_ui/locator_type.py
* 默认使用4个worker进行并行测试
* 文件下载处理暂不支持ie浏览器
* 无头浏览器暂不支持ie浏览器
* 项目
    * demoProject 例子项目
        
### 3、app ui测试
* 元素的显式等待时间默认为30s
* 封装的显式等待类型支持:page_objects/app_ui/wait_type.py
* 封装的定位类型支持:page_objects/app_ui/locator_type.py
* 项目
    * android 
        * demoProject 例子项目

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
* page_objects 页面映射对象
* pojo 存放自定义类对象
* test_data 测试所需的测试数据目录
* run_api_test.py 运行api测试脚本
* run_web_ui_test.py 运行web ui测试脚本
* run_app_ui_test.py 运行app ui测试脚本
* generate_api_test_report.py 生成api测试报告
* generateReport_web_ui_test_report.py 生成web ui测试报告
* generateReport_app_ui_test_report.py 生成app ui测试报告

# [编码规范]()
* 统一使用python 3.6.8
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
* @pytest.mark.usefixtures('func_name')

# [注意点]()
* 运行pytest时指定的目录内应当有conftest.py，方能在其他模块中使用。@allure.step会影响fixture，故在脚本中不使用@allure.step
* 由于web ui配置的驱动是直接设置在系统环境变量，app ui指定了混合应用的浏览器驱动，在运行app ui时appium有可能会读取到系统的环境变量的配置，故运行时请排查此情况
* 数据库操作，所有表操作均进行单表操作，如需多表查询，使用代码进行聚合
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

[![Stargazers over time](https://starchart.cc/yanchunhuo/AutomationTest.svg)](https://starchart.cc/yanchunhuo/AutomationTest)

[![Top Langs](https://profile-counter.glitch.me/yanchunhuo/count.svg)](https://github.com/yanchunhuo)