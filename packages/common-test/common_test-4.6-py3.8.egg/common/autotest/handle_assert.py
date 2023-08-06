import os

from loguru import logger
from common.autotest.handle_allure import allure_step
from common.data.data_process import DataProcess
from common.data.handle_common import req_expr, convert_json, extractor, is_not_bank


def assert_result(res: dict, expect_str: str):
    """ 预期结果实际结果断言方法
    :param res: 实际响应结果
    :param expect_str: 预期响应内容，从excel中读取
    return None
    """
    # 后置sql变量转换
    expect_str = req_expr(expect_str, DataProcess.response_dict)
    expect_dict = convert_json(expect_str)
    index = 0
    for k, v in expect_dict.items():
        # 获取需要断言的实际结果部分
        actual = extractor(res, k)
        index += 1
        logger.info(f'第{index}个断言,实际结果:{actual} | 预期结果:{v} \n断言结果 {actual == v}')
        allure_step(f'第{index}个断言', f'实际结果:{actual} = 预期结果:{v}')
        try:
            assert actual == v
        except AssertionError:
            raise AssertionError(f'第{index}个断言失败 -|- 实际结果:{actual} || 预期结果: {v}')

def assert_equals(res: str, expect_str: str,desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} = 预期结果:{expect_str}')
    try:
        assert res == expect_str
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} != 预期结果: {expect_str}')

def assert_contains(res, expect_str,desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} 包含 预期结果:{expect_str}')
    try:
        assert expect_str in res
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} 不包含 预期结果: {expect_str}')

def assert_Nobank(res, desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} 不为空')
    try:
        assert is_not_bank(res)
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} 为空')


def assert_not_contains(res, expect_str,desc:str='断言检查'):
    allure_step(f'{desc}', f'实际结果:{res} 不包含 预期结果:{expect_str}')
    try:
        assert expect_str not in res
    except AssertionError:
        raise AssertionError(f'{desc} |- 实际结果:{res} 包含 预期结果: {expect_str}')

def assert_scene_result(res, expect_dict):
    global actual

    index = 0
    for k, v in expect_dict.items():
        # 获取需要断言的实际结果部分
        try:
            actual = extractor(res, k)
            index += 1
            logger.info(f'第{index}个断言,实际结果:{actual} | 预期结果:{v} | 断言结果 {actual == v}')
            allure_step(f'第{index}个断言', f'实际结果:{actual} = 预期结果:{v}')

            assert actual == v
        except AssertionError:
            raise AssertionError(f'第{index}个断言失败 -|- 实际结果:{actual} || 预期结果: {v}')



if __name__ == '__main__':
    res = {'a':2,'b':3,'c':3,'g':6}
    except_dict = '{"$.a":2,"$.b":3,"$.c":3}'
    assert_result(res,except_dict)



