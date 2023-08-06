
import os
import re
import json
from jsonpath import jsonpath
from loguru import logger

from common.common.constant import Constant
from common.plugin.hooks_plugin import exec_func

def extractor(obj: dict, expr: str = '.', error_flag: bool = False) -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        if error_flag:
            logger.warning(f'{expr} - 提取不到内容！{e}')
        result = expr
    return result

def req_expr(content: str, data: dict = None, expr: str = '{(.*?)}') -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 在该项目中一般为响应字典，从字典取值出来
    :param expr: 查找用的正则表达式
    return content： 替换表达式后的字符串
    """
    if isinstance(content, str):
        content = content.replace('\\', '')
    else:
        content = str(content)
        content = content.replace('\\', '')
    for i in re.findall(expr, content):
        # TODO,自己修改的地方
        if get_system_key(f'{i}') is None:
            if str(extractor(data, i)) == f'{i}':
                content = content.replace('${' + f'{i}' + '}', Constant.DATA_NO_CONTENT)
            else:
                content = content.replace('${'+f'{i}'+'}', str(extractor(data, i)))
        else:
            content = content.replace('${'+f'{i}'+'}', str(get_system_key(f'{i}')))

    # 增加自定义函数得的调用，函数写在tools/hooks.py中
    for func in re.findall('@(.*?)@', content):
        try:
            content = content.replace(f'@{func}@', exec_func(func))
        except Exception as e:
            logger.error(e)
            continue
    return content



# 替换表格数据
def replace_data(data, cls):
    """
    替换数据
    :param data: 要进行替换的用例数据(字符串)
    :param cls:  测试类
    :return:
    使用方法：
    读取表格中data数据，调用此方法传入data数据和类名进行替换，再时使用eval转为json类型
    item['data'] = replace_data(item['data'], AddTestCase)
    params = eval(item['data'])
    """
    while re.search('#(.+?)#', data):
        res = re.search('#(.+?)#', data)
        item = res.group()
        attr = res.group(1)
        value = getattr(cls, attr)
        # 进行替换
        data = data.replace(item, str(value))
    return data


def convert_json(dict_str: str) -> dict:
    """
    :param dict_str: 长得像字典的字符串
    return json格式的内容
    """
    try:
        if 'None' in dict_str:
            dict_str = dict_str.replace('None', 'null')
        if 'True' in dict_str:
            dict_str = dict_str.replace('True', 'true')
        if 'False' in dict_str:
            dict_str = dict_str.replace('False', 'false')

        dict_str = json.loads(dict_str)

    except Exception as e:
        if 'null' in dict_str:
            dict_str = dict_str.replace('null', 'None')
        if 'true' in dict_str:
            dict_str = dict_str.replace('true', 'True')
        if 'false' in dict_str:
            dict_str = dict_str.replace('false', 'False')

        dict_str = eval(dict_str)

        logger.error(e)
    return dict_str

def get_system_key(str_key,):
    """
    从环境变量中获取值
    :param str_key:
    :return:
    """
    temp = None
    if os.getenv(str_key.strip()) is not None:
        temp = os.getenv(str_key.strip())
    else:
        if os.getenv(str_key.lower().strip()) is not None:
            temp = os.getenv(str_key.lower().strip())
    return temp


def set_system_key(str_key,str_value):
    """
    把值设置到环境变量中
    :param str_key:
    :param str_value:
    :return:
    """
    if str_value is not None and isinstance(str_value, str):
        os.environ[str_key.lower().strip()] = str_value.strip()
    if str_value is not None and isinstance(str_value,dict):
        os.environ[str_key.lower().strip()] = str(str_value)



def is_bank(_str):
    if _str is None:
        return True
    if _str.strip() == '':
        return True
    return False

def is_not_bank(_str):
    if _str is None:
        return False
    if _str.strip() == '':
        return False
    return True






if __name__ == '__main__':
    # 实例, 调用无参数方法 get_current_time'
    # print(req_expr("&33333&87334&bbb&333&cccc1&@get_current_time()@",{}))
    print(get_system_key('test'))
    #
    # # result = exec_func("get_current_time()")
    # # print(req_expr("iiieee"))
    # # print(result)
    # # # 调用有参数方法 sum_data
    # # print(exec_func("sum_data(1,3)"))
    #
    # print(get_system_key("33333"))
    # dict={'333',"8333"}
    # print(is_bank(dict))

