#
# decorator.py
# @author yanchunhuo
# @description 
# @created 2024-07-25T10:37:58.417Z+08:00
# @last-modified 2024-07-25T10:44:56.394Z+08:00
# github https://github.com/yanchunhuo

from common.date_time_tool import DateTimeTool
from urllib.parse import urlparse, parse_qs
import inspect
import ujson

def api_log(api=None, print_params=True, print_response=True, ensure_ascii=False):
    """

    Args:
        api: do_request实例
        print_params: 是否打印请求参数
        print_response: 是否打印响应结果
        ensure_ascii: json数据中非ASCII字符是否被转义未ASCII字符形式

    Returns:

    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # 获取原始函数所在模块层级以及自身
            module_list = get_package_hierarchy(func)
            module_list.append(func.__name__)
            title = ''
            for name in module_list:
                title += f'【{name}】'
            # 调用原始函数
            result = func(self, *args, **kwargs)

            # 调用原始函数之后打印日志
            print('%s%s【请求url】:%s' % (
                DateTimeTool.get_now_time(), title, getattr(self, api).get_url() + self.path))
            print('%s%s【请求头】:%s' % (
                DateTimeTool.get_now_time(), title,
                ujson.dumps(getattr(self, api).getHeaders(), ensure_ascii=ensure_ascii)))

            if print_params:
                response = getattr(self, api).get_response()
                params = response.request.body
                if params is None:
                    if response.request.method in ['GET', 'DELETE']:
                        url = response.request.url
                        parsed_url = urlparse(url)
                        params = parse_qs(parsed_url.query)
                    else:
                        params = None
                else:
                    try:
                        params = ujson.loads(params.decode('utf-8'))
                    except UnicodeDecodeError as e:
                        params = params
                print('%s%s【请求参数】:%s' % (
                    DateTimeTool.get_now_time(), title, params))
            if print_response:
                print('%s%s【响应信息】:%s' % (DateTimeTool.get_now_time(), title, result.body))
            print('%s%s【当前cookies】:%s' % (
                DateTimeTool.get_now_time(), title, ujson.dumps(getattr(self, api).getCookies())))
            print('%s%s【cURL】:%s' % (
                DateTimeTool.get_now_time(), title, getattr(self, api).get_curl_command()))

            return result

        return wrapper

    return decorator


# 获取函数的层级
def get_package_hierarchy(func):
    module = inspect.getmodule(func)
    packages = module.__package__.split('.')
    for p in packages:
        if p == 'api':
            packages = packages[packages.index('api') + 1:]
            break

    return packages
