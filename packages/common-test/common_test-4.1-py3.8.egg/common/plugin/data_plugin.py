import json

from common.data.handle_common import req_expr, convert_json


class DataPlugin(object):
    @classmethod
    def convert_json(self, _temp, _replace: bool = True):
        """
        任意的数据类型转换成Json
        :param _temp:
        :param _replace: 是否清洗数据
        :return:
        """
        content = _temp
        if isinstance(_temp, str):
            content = json.loads(content)
        else:
            content = json.dumps(_temp)
        if _replace:
            content = req_expr(content)
        return content

    @classmethod
    def json_convert_dict(self, _json, _replace: bool = True) -> dict:
        """
              Json字符串转换为字典
              :param _json:
              :param _replace: 是否清洗数据
              :return:
              """
        if _replace:
            _json = req_expr(_json)
        return convert_json(_json)



if __name__ == '__main__':
    str1 = '{"listData": "333","strData": "test python obj 2 json"}'
    print(DataPlugin.convert_json(str1))





