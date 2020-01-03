# 作者 yanchunhuo
# 创建时间 2019/12/26 9:17
# github https://github.com/yanchunhuo

class APP_UI_Devices_Info:
    def __init__(self):
        self.devices_desc = []
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
        self.appPackage = None
        self.appActivity = None
        self.app = None

    def get_devices_info(self):
        devices_info = []
        for i in range(len(self.devices_desc)):
            device_info={}
            device_info.update({'device_desc':self.devices_desc[i].strip()})
            device_info.update({'server_port':self.server_ports[i].strip()})
            device_info.update({'server_ip':self.server_ips[i].strip()})
            device_info.update({'system_auth_alert_label': self.system_auth_alert_labels[i]})
            # 构建desired_capabilities
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
            if self.appActivity and self.appPackage:
                desired_capabilities.update({'appActivity': self.appActivity.strip()})
                desired_capabilities.update({'appPackage': self.appPackage.strip()})
            if self.app:
                desired_capabilities.update({'app': self.app.strip()})
            device_info.update({'capabilities':desired_capabilities})
            # 完成一台设备构建
            devices_info.append(device_info)
        return devices_info