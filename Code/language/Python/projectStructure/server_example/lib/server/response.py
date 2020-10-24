# coding: utf-8
# Author: wanhui0729@gmail.com
import json
import logging

# 返回码
class CODE(object):
    OK = 0  # OK
    INNER_WRONG = 1  # 内部错误


class Response(object):
    def __init__(self):
        self._response_dict = {}
        self._logger = logging.getLogger(__name__)
        self.code = None
        self.message = None

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._response_dict[name] = value

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__[name]
        else:
            return self._response_dict[name]

    def _message_log_summary(self, message, is_error):
        self.message = message
        if is_error:
            self._logger.error(message)
        else:
            self._logger.info(message)

    def has_result(self):
        return self.code is not None

    def ok(self, message):
        self.code = CODE.OK
        self._message_log_summary(message, is_error=False)

    def error(self, message):
        self.code = CODE.INNER_WRONG
        self._message_log_summary(message, is_error=True)


    def validate_response(self, OutItem):
        """
            args:
                OutItem: fastapi 定义的接口返回数据结构
            return:
                json: 返回校验后的数据格式
        """
        # 校验返回字典结构: {"mess".., "data": {嵌套字典也可以校验}..}
        resp_json = OutItem.validate(self._response_dict)
        # 返回 json 格式,避免前端再反序列化数据
        return resp_json.dict()