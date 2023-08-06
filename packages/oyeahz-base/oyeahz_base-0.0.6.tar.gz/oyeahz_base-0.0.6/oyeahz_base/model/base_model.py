# coding=utf-8

class BaseResponse:
    def __init__(self):
        self.error_code = -1
        self.error_msg = ""
        self.data = {}


class ParamErrorResponse:
    def __init__(self):
        self.error_code = 499
        self.error_msg = "参数异常，请稍候再试"
        self.data = None


class SeverErrorResponse:
    def __init__(self):
        self.error_code = 500
        self.error_msg = "系统开小差了"
        self.data = None


class SessionInvalidResponse:
    def __init__(self):
        self.error_code = 600
        self.error_msg = "会话过期，请重新登录"
        self.data = None
