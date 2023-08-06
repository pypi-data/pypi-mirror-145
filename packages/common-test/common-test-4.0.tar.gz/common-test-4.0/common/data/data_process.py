import ast
import json
import os
from os import path
from loguru import logger
from common.autotest.handle_allure import allure_step
from common.config.config import TEST_FILE_PATH, TEST_DATA_PATH
from common.data.handle_common import req_expr, convert_json
from common.file.ReadFile import get_yaml_config


class DataProcess:
    response_dict = {}
    @classmethod
    def save_response(cls, key: str, value: object) -> None:
        """
        保存实际响应
        :param key: 保存字典中的key，一般使用用例编号
        :param value: 保存字典中的value，使用json响应
        """
        cls.response_dict[key] = value
        logger.info(f'添加key: {key}, 对应value: {value}')


    @classmethod
    def handle_path(cls, path_str: str) -> str:
        """路径参数处理
        :param path_str: 带提取表达式的字符串 /&$.case_005.data.id&/state/&$.case_005.data.create_time&
        上述内容表示，从响应字典中提取到case_005字典里data字典里id的值，假设是500，后面&$.case_005.data.create_time& 类似，最终提取结果
        return  /511/state/1605711095
        """
        # /&$.case.data.id&/state/&$.case_005.data.create_time&
        return req_expr(path_str, cls.response_dict)

    @classmethod
    def handle_header(cls, token) -> dict:
        """处理header
        :param token: 写： 写入token到header中， 读： 使用带token的header， 空：使用不带token的header
        return
        """
        if token is None or str(token) == '':
            header = get_yaml_config('$.common.request_headers')
        else:
            if isinstance(token, str) and token.find('$.common') != -1:
                header = get_yaml_config(token)
            else:
                header = token
        if token == '读':
            header = req_expr(header.copy())
        else:
            header = req_expr(header)
        if isinstance(header, dict):
            return header
        else:
            return ast.literal_eval(header)

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """file对象处理方法
        :param file_obj: 上传文件使用，格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        实例- 单个文件: &file&D:
        """
        d = path.dirname(__file__)
        # 返回当前d文件的父目录地址
        parent_path = os.path.dirname(d)

        if file_obj == '' or file_obj is None:
            return
        for k, v in convert_json(file_obj).items():
            # 多文件上传
            if isinstance(v, list):
                files = []
                for ex_path in v:
                    all_path = os.sep.join([TEST_FILE_PATH,ex_path])
                    files.append((k, (open(all_path, 'rb'))))
                    # print(all_path)

            else:
                # 单文件上传
                all_path = os.sep.join([TEST_FILE_PATH, v])
                files = {k: open(all_path, 'rb')}
            return files

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """请求数据处理
        :param variable: 请求数据，传入的是可转换字典/json的字符串,其中可以包含变量表达式
        return 处理之后的json/dict类型的字典数据
        """
        if variable == '':
            return
        if isinstance(variable, str) and variable.find(".json",len(variable)-5) != -1:
            _path = path.join(TEST_DATA_PATH, variable, )
            with open(_path, "r") as json_file:
                variable = json.load(json_file)
        data = req_expr(variable, cls.response_dict)
        variable = convert_json(data)
        return variable

    @classmethod
    def handle_sql(cls, sql: str, db: object):
        """处理sql，并将结果写到响应字典中"""
        if sql :
            sql = req_expr(sql, cls.response_dict)
            allure_step('运行sql', sql)
            logger.info(sql)
            # 查后置sql
            result = db.fetch_one(sql)
            allure_step('sql执行结果', {"sql_result": result})
            logger.info(f'结果：{result}')
            if result:
                # 将查询结果添加到响应字典里面，作用在，接口响应的内容某个字段 直接和数据库某个字段比对，在预期结果中
                # 使用同样的语法提取即可
                cls.response_dict.update(result)
        else:
            sql = None
            return



if __name__ == '__main__':
    da=DataProcess()
     # file_obj = '{"files":["data/pic002.jpeg"]}'
     # print(da.handler_files(file_obj))
    # print(get_yaml_config('$.common.request_headers'))
    # str='4883838/38384'
    # if str.find(".json", len(str) - 5) != -1:
    #     print("11")
    # else:
    #     print("222")




