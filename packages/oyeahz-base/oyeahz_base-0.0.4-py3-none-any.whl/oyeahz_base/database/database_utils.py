# coding=utf-8
import pymysql
import re
from pymysql.connections import Connection
from oyeahz_base.logger.xlogger import logger


# 获取mysql数据库实例
def get_database(host: str, user: str, password: str, database: str) -> Connection:
    db = None
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    except Exception as obj:
        logger.error(obj)
    return db


# 判断数据库中表是否存在
def table_exists(database: Connection, table_name: str) -> bool:
    if database is None:
        return False
    try:
        cursor = database.cursor()
        show_table_sql = "show tables;"
        cursor.execute(show_table_sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return True
        else:
            return False
    except Exception as obj:
        logger.error(obj)
