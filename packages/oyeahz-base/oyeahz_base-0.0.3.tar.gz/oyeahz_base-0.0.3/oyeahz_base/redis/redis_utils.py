# coding=utf-8
import redis
from redis.client import Redis


# 获取redis实例
def get_redis(host: str, port: int) -> Redis:
    redis.StrictRedis(host=host, port=port, db=0)
