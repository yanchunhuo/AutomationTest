# 作者 yanchunhuo
# 创建时间 2019/12/26 11:15
# github https://github.com/yanchunhuo
from pojo.app_ui_devices_info import APP_UI_Devices_Info
import configparser as ConfigParser

class Read_APP_UI_Devices_Info(object):
    __instance=None
    __inited=None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
        return cls.__instance

    def __init__(self,filepath):
        if self.__inited is None:
            self.devices_info=self._read_devices_info(filepath)
            self.__inited=True

    def _read_devices_info(self, filepath):
        config = ConfigParser.ConfigParser()
        config.read(filepath,encoding='utf-8')
        devices_info = APP_UI_Devices_Info()
        get_lambda=lambda info:list(filter(None,info.split('||'))) if info else []
        devices_info.devices_desc=get_lambda(config.get('devices_info','devices_desc',fallback=''))
        devices_info.app_ui_configs = get_lambda(config.get('devices_info', 'app_ui_configs', fallback=''))
        api_configs=[]
        get_api_config=lambda tmp_api_config:list(filter(None,tmp_api_config.split('&&'))) if tmp_api_config else []
        for tmp_api_config in get_lambda(config.get('devices_info','api_configs',fallback='')):
            api_configs.append(get_api_config(tmp_api_config))
        devices_info.api_configs = api_configs
        devices_info.server_ports=get_lambda(config.get('devices_info','server_ports',fallback=''))
        devices_info.server_ips = get_lambda(config.get('devices_info', 'server_ips', fallback=''))
        system_auth_alert_labels=[]
        get_system_auth_alert_label=lambda tmp_system_auth_alert_label:list(filter(None,tmp_system_auth_alert_label.split('&&'))) if tmp_system_auth_alert_label else []
        for tmp_system_auth_alert_label in get_lambda(config.get('devices_info','system_auth_alert_labels',fallback='')):
            system_auth_alert_labels.append((get_system_auth_alert_label(tmp_system_auth_alert_label)))
        devices_info.is_enable_system_auth_check = get_lambda(config.get('devices_info', 'is_enable_system_auth_check', fallback=''))
        devices_info.system_auth_alert_labels=system_auth_alert_labels
        devices_info.udids=get_lambda(config.get('devices_info','udids',fallback=''))
        devices_info.platformNames = get_lambda(config.get('devices_info', 'platformNames',fallback=''))
        devices_info.automationNames = get_lambda(config.get('devices_info', 'automationNames', fallback=''))
        devices_info.platformVersions = get_lambda(config.get('devices_info', 'platformVersions', fallback=''))
        devices_info.deviceNames = get_lambda(config.get('devices_info', 'deviceNames', fallback=''))
        devices_info.chromeDriverPorts = get_lambda(config.get('devices_info', 'chromeDriverPorts', fallback=''))
        devices_info.chromeDriverPaths = get_lambda(config.get('devices_info', 'chromeDriverPaths', fallback=''))
        devices_info.recreateChromeDriverSessions = get_lambda(config.get('devices_info', 'recreateChromeDriverSessions', fallback=''))
        devices_info.nativeWebScreenshots = get_lambda(config.get('devices_info', 'nativeWebScreenshots', fallback=''))
        devices_info.systemports=get_lambda(config.get('devices_info','systemports', fallback=''))
        devices_info.wdaLocalPorts = get_lambda(config.get('devices_info', 'wdaLocalPorts', fallback=''))
        devices_info.wdaLocalPorts = get_lambda(config.get('devices_info', 'wdaLocalPorts', fallback=''))
        devices_info.appActivitys = get_lambda(config.get('devices_info','appActivitys',fallback=''))
        devices_info.appPackages = get_lambda(config.get('devices_info','appPackages',fallback=''))
        devices_info.bundleIds = get_lambda(config.get('devices_info','bundleIds',fallback=''))
        devices_info.apps_dirs = get_lambda(config.get('devices_info','apps_dirs',fallback=''))
        devices_info.apps_urls = get_lambda(config.get('devices_info', 'apps_urls', fallback=''))
        devices_info.noSigns = get_lambda(config.get('devices_info','noSigns',fallback=''))
        devices_info.fullResets = get_lambda(config.get('devices_info', 'fullResets', fallback=''))
        devices_info.noResets = get_lambda(config.get('devices_info', 'noResets', fallback=''))
        return devices_info.get_devices_info()