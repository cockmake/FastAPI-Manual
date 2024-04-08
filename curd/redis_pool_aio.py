from redis import asyncio as aioredis

from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

REDIS_CONFIG = {
    # "max_connections": None,  # 一般不用设置
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_DB,
    "password": REDIS_PASSWORD,
    "decode_responses": True,  # 有时为了提高性能，可以不解码
}
redis_pool_aio = aioredis.ConnectionPool(**REDIS_CONFIG)
