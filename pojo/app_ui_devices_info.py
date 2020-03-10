# 作者 yanchunhuo
# 创建时间 2019/12/26 9:17
from base.read_httpserver_config import Read_Http_Server_Config
import os

class APP_UI_Devices_Info:
    def __init__(self):
        self.devices_desc = []
        self.app_ui_configs=[]
        self.server_ports = []
        self.server_ips = []
        self.system_auth_alert_labels = []
        self.udids = []
        self.platformNames = []
        self.automationNames = []
        self.platformVersions = []
        self.deviceNames = []
        self.chromeDriverPorts = []
        self.systemports = []
        self.wdaLocalPorts = []
        self.appPackages = []
        self.appActivitys = []
        self.apps_dirs = []
        self.noSigns=[]
        self.fullResets=[]

    def get_devices_info(self):
        devices_info = []
        local_ip = Read_Http_Server_Config().httpserver_config.local_ip
        httpserver_port = Read_Http_Server_Config().httpserver_config.httpserver_port
        for i in range(len(self.devices_desc)):
            device_info={}
            device_info.update({'device_desc':self.devices_desc[i].strip()})
            device_info.update({'app_ui_config': self.app_ui_configs[i].strip()})
            device_info.update({'server_port':self.server_ports[i].strip()})
            device_info.update({'server_ip':self.server_ips[i].strip()})
            if self.system_auth_alert_labels:
                device_info.update({'system_auth_alert_label': self.system_auth_alert_labels[i]})
            # 构建desired_capabilities
            a_device_capabilities_num=0
            a_device_appActivitys=[]
            a_device_appPackages=[]
            a_device_apps=[]
            if self.appActivitys and self.appPackages:
                a_device_appActivitys=self.appActivitys[i].split('&&')
                a_device_appPackages=self.appPackages[i].split('&&')
                a_device_capabilities_num=len(a_device_appActivitys)
            if self.apps_dirs:
                a_device_capabilities_num=len(self.apps_dirs)
                paths=os.walk(self.apps_dirs[i].strip())
                for dirPath,dirName,fileNames in paths:
                    for fileName in fileNames:
                        a_device_apps.append(('http://%s:%s/%s/%s')%(local_ip,httpserver_port,self.apps_dirs[i].strip(),fileName))
            a_devices_desired_capabilities=[]
            for j in range(a_device_capabilities_num):
                desired_capabilities={}
                desired_capabilities.update({'udid':self.udids[i].strip()})
                desired_capabilities.update({'platformName': self.platformNames[i].strip()})
                if len(self.automationNames):
                    desired_capabilities.update({'automationName': self.automationNames[i].strip()})
                desired_capabilities.update({'platformVersion': self.platformVersions[i].strip()})
                if len(self.deviceNames):
                    desired_capabilities.update({'deviceName': self.deviceNames[i].strip()})
                desired_capabilities.update({'chromeDriverPort':self.chromeDriverPorts[i].strip()})
                desired_capabilities.update({'systemport': self.systemports[i].strip()})
                if len(self.wdaLocalPorts):
                    desired_capabilities.update({'wdaLocalPort': self.wdaLocalPorts[i].strip()})
                if self.appActivitys and self.appPackages:
                    desired_capabilities.update({'appActivity': a_device_appActivitys[j].strip()})
                    desired_capabilities.update({'appPackage': a_device_appPackages[j].strip()})
                else:
                    desired_capabilities.update({'appActivity': ''})
                    desired_capabilities.update({'appPackage': ''})
                if self.apps_dirs:
                    desired_capabilities.update({'app': a_device_apps[j]})
                if len(self.noSigns):
                    noSign=False
                    if 'true'==self.noSigns[i].strip().lower():
                        noSign=True
                    desired_capabilities.update({'noSign':noSign})
                if len(self.fullResets):
                    fullReset=False
                    if 'true'==self.fullResets[i].strip().lower():
                        fullReset=True
                    desired_capabilities.update({'fullReset':fullReset})
                a_devices_desired_capabilities.append(desired_capabilities)
            device_info.update({'capabilities': a_devices_desired_capabilities})
            # 完成一台设备构建
            devices_info.append(device_info)
        return devices_info