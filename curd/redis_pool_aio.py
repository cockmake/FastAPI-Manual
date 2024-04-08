from redis import asyncio as aioredis

from settings import REDIS_POOL_SIZE, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

REDIS_CONFIG = {
    "max_connections": REDIS_POOL_SIZE,  # 最大连接数比最大可工作线程数多1
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_DB,
    "password": REDIS_PASSWORD,
    "decode_responses": True,  # 有时为了提高性能，可以不解码
}
redis_pool_aio = aioredis.ConnectionPool(**REDIS_CONFIG)
