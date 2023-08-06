import allure
import json


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)


def allure_feature(feature: str) -> None:
    """allure中显示的用例模块"""
    allure.dynamic.feature(feature)

def allure_severity(severity_level: str) -> None:
    """allure中显示的用例等级"""
    allure.dynamic.severity(convert_severity(severity_level))


def allure_step(step: str, content: str) -> None:
    """
    :param step: 步骤及附件名称
    :param content: 附件内容
    """
    with allure.step(step):
        allure.attach(json.dumps(content, ensure_ascii=False, indent=4), step, allure.attachment_type.TEXT)

def convert_severity(_str):
    return _str.replace("P0", "critical").replace("P1", "normal") \
        .replace("P2", "minor").replace("P3", "trivial")







