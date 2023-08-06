import json

from typing import List


class response:
    def __init__(self, data: dict, msg: str, code: str):
        self.data = data
        self.msg = msg
        self.code = code

    def parseJonsByte(self) -> List[bytes]:
        """
        输出标准返回体
        :return: 按照阿里函数计算格式，返回标准的List[bytes] 格式
        """
        dic_ = {
            'data': self.data,
            'msg': self.msg,
            'code': self.code
        }
        json_ = json.dumps(dic_)
        json_byte = bytes(json_, encoding="utf8")
        return [json_byte]
