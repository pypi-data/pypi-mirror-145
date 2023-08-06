# coding=utf-8
from oyeahz_base.logger.xlogger import logger
from flask import Request, Response
import json


# 获取query参数
def get_query_param(req: Request, key):
    param = req.args.get(key)
    if param is None:
        raise Exception(f'key: %s error!' % key)
    return param


# 获取query参数，不抛异常返回None
def safe_get_query_param(req: Request, key):
    param = None
    try:
        param = req.args.get(key)
    except Exception as obj:
        logger.error(obj)
    return param


# 获取get_data里的body数据
def get_post_param(req: Request, key):
    post_body = req.get_data()
    body_data = json.loads(post_body)
    return body_data[key]


# 获取get_data里的body数据，不抛异常返回None
def safe_get_post_param(req: Request, key):
    param = None
    try:
        post_body = req.get_data()
        body_data = json.loads(post_body)
        param = body_data[key]
    except Exception as obj:
        logger.error(obj)
    return param


# 把Model转成响应
def make_response(resp: Response) -> str:
    return json.dumps(resp, default=lambda obj: obj.__dict__)
