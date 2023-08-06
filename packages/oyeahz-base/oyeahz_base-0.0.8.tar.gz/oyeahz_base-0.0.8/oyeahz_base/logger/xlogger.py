# coding=utf-8
import logging
import sys
from os.path import join, dirname
from datetime import datetime


def today():
    return datetime.now().strftime('%Y_%m_%d')


def set_up_logger():
    # 获取logger实例，如果参数为空则返回root logger
    _logger = logging.getLogger("Oyeahz")

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日志
    file_handler = logging.FileHandler(join(dirname(dirname(__file__)), f"oyeahz_{today()}.log"), encoding='utf-8')
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    _logger.setLevel(logging.INFO)

    return _logger


logger = set_up_logger()
