# 作者 yanchunhuo
# 创建时间 2019/12/26 9:17
# github https://github.com/yanchunhuo
from base.read_httpserver_config import Read_Http_Server_Config
import os

class APP_UI_Devices_Info:
    def __init__(self):
        self.devices_desc = []
        self.app_ui_configs = []
        self.api_configs = []
        self.server_ports = []
        self.server_ips = []
        self.system_auth_alert_labels = []
        self.is_enable_system_auth_check = []
        self.udids = []
        self.platformNames = []
        self.automationNames = []
        self.platformVersions = []
        self.deviceNames = []
        self.chromeDriverPorts = []
        self.chromeDriverPaths = []
        self.recreateChromeDriverSessions = []
        self.nativeWebScreenshots = []
        self.systemports = []
        self.wdaLocalPorts = []
        self.appPackages = []
        self.appActivitys = []
        self.bundleIds = []
        self.apps_dirs = []
        self.apps_urls = []
        self.noSigns = []
        self.fullResets = []
        self.noResets = []

    def get_devices_info(self):
        devices_info = []
        local_ip = Read_Http_Server_Config().httpserver_config.local_ip
        httpserver_port = Read_Http_Server_Config().httpserver_config.httpserver_port
        for i in range(len(self.devices_desc)):
            device_info = {}
            device_info.update({'device_desc': self.devices_desc[i].strip()})
            device_info.update({'app_ui_config': self.app_ui_configs[i].strip()})
            if self.api_configs:
                device_info.update({'api_config': self.api_configs[i]})
            device_info.update({'server_port': self.server_ports[i].strip()})
            device_info.update({'server_ip': self.server_ips[i].strip()})
            if self.system_auth_alert_labels:
                device_info.update({'system_auth_alert_label': self.system_auth_alert_labels[i]})
            device_info.update({'is_enable_system_auth_check': self.is_enable_system_auth_check[i]})
            # 构建desired_capabilities
            a_device_capabilities_num = 0
            a_device_appActivitys = []
            a_device_appPackages = []
            a_device_bundleIds = []
            a_device_apps = []
            if len(self.appActivitys) and len(self.appPackages):
                a_device_appActivitys = self.appActivitys[i].split('&&')
                a_device_appPackages = self.appPackages[i].split('&&')
                a_device_capabilities_num = len(a_device_appActivitys)
            if len(self.bundleIds):
                a_device_bundleIds = self.bundleIds[i].split('&&')
                a_device_capabilities_num = len(a_device_bundleIds)
            if len(self.apps_dirs):
                paths = os.walk(self.apps_dirs[i].strip())
                for dirPath, dirName, fileNames in paths:
                    for fileName in fileNames:
                        a_device_apps.append(
                            ('http://%s:%s/%s/%s') % (local_ip, httpserver_port, self.apps_dirs[i].strip(), fileName))
                a_device_capabilities_num = len(a_device_apps)
            if len(self.apps_urls):
                a_device_apps = self.apps_urls[i].split('&&')
                a_device_capabilities_num = len(a_device_apps)
            a_devices_desired_capabilities = []
            for j in range(a_device_capabilities_num):
                desired_capabilities = {}
                desired_capabilities.update({'udid': self.udids[i].strip()})
                desired_capabilities.update({'platformName': self.platformNames[i].strip()})
                if len(self.automationNames):
                    desired_capabilities.update({'automationName': self.automationNames[i].strip()})
                desired_capabilities.update({'platformVersion': self.platformVersions[i].strip()})
                if len(self.deviceNames):
                    desired_capabilities.update({'deviceName': self.deviceNames[i].strip()})
                if len(self.chromeDriverPorts):
                    desired_capabilities.update({'chromedriverPort': self.chromeDriverPorts[i].strip()})
                if len(self.chromeDriverPaths):
                    desired_capabilities.update({'chromedriverExecutable':self.chromeDriverPaths[i].strip()})
                if len(self.recreateChromeDriverSessions):
                    recreateChromeDriverSessions_value=False
                    if 'true' == self.recreateChromeDriverSessions[i].strip().lower():
                        recreateChromeDriverSessions_value=True
                    desired_capabilities.update({'recreateChromeDriverSessions':recreateChromeDriverSessions_value})
                if len(self.nativeWebScreenshots):
                    nativeWebScreenshot=False
                    if 'true' == self.nativeWebScreenshots[i].strip().lower():
                        nativeWebScreenshot=True
                    desired_capabilities.update({'nativeWebScreenshot':nativeWebScreenshot})
                desired_capabilities.update({'systemport': self.systemports[i].strip()})
                if len(self.wdaLocalPorts):
                    desired_capabilities.update({'wdaLocalPort': self.wdaLocalPorts[i].strip()})
                if len(self.appActivitys) and len(self.appPackages):
                    desired_capabilities.update({'appActivity': a_device_appActivitys[j].strip()})
                    desired_capabilities.update({'appPackage': a_device_appPackages[j].strip()})
                if len(self.bundleIds):
                    desired_capabilities.update({'bundleId': a_device_bundleIds[j].strip()})
                if len(self.apps_dirs) or len(self.apps_urls):
                    desired_capabilities.update({'app': a_device_apps[j].strip()})
                if len(self.noSigns):
                    noSign = False
                    if 'true' == self.noSigns[i].strip().lower():
                        noSign = True
                    desired_capabilities.update({'noSign': noSign})
                if len(self.fullResets):
                    fullReset = False
                    if 'true' == self.fullResets[i].strip().lower():
                        fullReset = True
                    desired_capabilities.update({'fullReset': fullReset})
                if len(self.noResets):
                    noReset = False
                    if 'true' == self.noResets[i].strip().lower():
                        noReset = True
                    desired_capabilities.update({'noReset': noReset})
                a_devices_desired_capabilities.append(desired_capabilities)
            device_info.update({'capabilities': a_devices_desired_capabilities})
            # 完成一台设备构建
            devices_info.append(device_info)
        return devices_info