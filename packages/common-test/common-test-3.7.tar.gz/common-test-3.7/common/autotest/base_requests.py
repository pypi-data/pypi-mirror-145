import requests
from loguru import logger
from common.autotest.handle_allure import allure_title, allure_feature, allure_step, allure_severity
from common.autotest.handle_assert import assert_equals
from common.common.constant import Constant
from common.data.data_process import DataProcess
from common.data.handle_common import extractor, get_system_key, req_expr, set_system_key
from common.file.ReadFile import ReadFile, get_yaml_ApiSchemal


class BaseRequest(object):
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def http_request(cls, url, method, parametric_key, header=None, data=None, file=None, cookie=None) -> object:
        """
        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()

        if parametric_key == 'params':
            res = session.request(method=method, url=url, params=data, headers=header, cookies=cookie)
        elif parametric_key == 'data':
            res = session.request(method=method, url=url, data=data, files=file, headers=header, cookies=cookie)
        elif parametric_key == 'json':
            res = session.request(method=method, url=url, json=data, files=file, headers=header, cookies=cookie)
        else:
            raise ValueError('可选关键字为params, json, data')
        logger.info(f'\n最终请求地址:{res.url}\n请求方法:{method}\n请求头:{header}\n请求参数:{data}\n上传文件:{file}\n响应数据:{res.text}')
        return res

    @classmethod
    def send_request(cls, case: list, host: str = 'host') -> object:
        """处理case数据，转换成可用数据发送请求
        :param case: 读取出来的每一行用例内容，可进行解包
        :param env: 环境名称 默认使用config.yaml server下的 dev 后面的基准地址
        return: 响应结果， 预期结果
        """
        case_number, case_title,case_feature, case_severity, path, token, method, parametric_key, file_obj, data, sql, expect, is_save = case
        logger.debug(f"用例进行处理前数据: \n 接口路径: {path} \n 请求参数: {data} \n 后置sql: {sql} \n 预期结果: {expect} \n 保存响应: {is_save}")
        # allure报告 用例标题
        allure_title(case_title)
        # allure报告用例优先级
        allure_severity(case_severity)
        # allure报告 用例模块
        allure_feature(case_feature)
        # 处理url、header、data、file、的前置方法
        url = DataProcess.handle_path(path)
        if url.find("http") == -1:
            url = get_system_key(host) + DataProcess.handle_path(path)
        cls._convert_url(url)
        logger.info("url:",url)
        allure_step('请求地址', url)
        header = DataProcess.handle_header(token)
        allure_step('请求头', header)
        data = DataProcess.handle_data(data)
        allure_step('请求参数', data)
        file = DataProcess.handler_files(file_obj)
        if file is not None:
            allure_step('上传文件', file_obj)
        # 发送请求
        res = cls.http_request(url, method, parametric_key, header, data, file)
        # 请求后做的事
        allure_step('响应耗时(s)', res.elapsed.total_seconds())
        allure_step('响应状态码', res.status_code)
        allure_step('响应内容', res.text)
        if get_system_key(Constant.RESPONSE_CODE) is not None and res.status_code > int(get_system_key(Constant.RESPONSE_CODE)):
            assert_equals('请求状态码返回错误', f'实际状态码:{res.status_code}', '状态码检查')
        # 响应后操作
        if token == '写':
            DataProcess.have_token['Authorization'] = extractor(res.json(), ReadFile.get_config_value('$.expr.token'))
            allure_step('请求头中添加Token', DataProcess.have_token)
        # 保存用例的实际响应
        if is_save == "yes":
            DataProcess.save_response(case_number, res.json())
        allure_step('存储实际响应', DataProcess.response_dict)
        return res.json(), expect, sql

    @classmethod
    def api_exec(cls, schemal_key, data=None, header=None, file=None, cookie=None, host: str = 'host') -> object:
        """处理case数据，转换成可用数据发送请求
        :param case: 读取出来的每一行用例内容，可进行解包
        :param env: 环境名称 默认使用config.yaml server下的 dev 后面的基准地址
        return: 响应结果， 预期结果
        """
        schemal_data = get_yaml_ApiSchemal(schemal_key)
        url = DataProcess.handle_path(schemal_data['url'])
        if url.find("http") == -1:
            url = get_system_key(host) + DataProcess.handle_path(url)
        cls._convert_url(url)
        allure_step('请求地址', url)
        if data == str:
            data = DataProcess.handle_data(data)
        header = DataProcess.handle_header(header)
        allure_step('请求头', header)
        data = DataProcess.handle_data(data)
        allure_step('请求参数', data)
        file = DataProcess.handler_files(file)
        if file is not None:
            allure_step('上传文件', file)
        # 发送请求
        res = cls.http_request(url, schemal_data['method'], schemal_data['datatype'], header, data, file, cookie)
        # 请求后做的事
        allure_step('响应耗时(s)', res.elapsed.total_seconds())
        allure_step('响应状态码', res.status_code)
        allure_step('响应内容', res.text)
        if get_system_key(Constant.RESPONSE_CODE) is not None and res.status_code > int(get_system_key('responseCode')):
            assert_equals('请求状态码返回错误', f'实际状态码:{res.status_code}', '状态码检查')
        return res

    @classmethod
    def _convert_url(self,url):
        _url = url.replace("//", '####').split('/')
        _newurl = '';
        for i in range(len(_url)):
            if _url[i].find(Constant.DATA_NO_CONTENT) == -1:
                _newurl = _newurl + _url[i] + '/'
        _newurl = _newurl.replace("//", "/").replace("####", "//")
        return _newurl


if __name__ == '__main__':
    set_system_key('host',"http://178.83.17.12")
    set_system_key('test2',"AAAA")
    set_system_key('name', "name")
    set_system_key('sex', "sex")
    url="http://127.0.0.1/AAA&在DataBus中未提取到内容!!!&在DataBus中未提取到内容!!!/zhangsan=在DataBus中未提取到内容!!!/lisi/zhangsan在DataBus中未提取到内容!!!/AAA在DataBus中未提取到内容!!!/在DataBus中未提取到内容!!!?id=5/test/333在DataBus中未提取到内容!!!/"
    print(BaseRequest.convert_url(url))








