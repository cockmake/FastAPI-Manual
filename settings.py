# 项目配置文件

# System
CPU_CORES = 2
THREAD_NUM = 10  # 可以稍微大一点
SERVER_PORT = 5003

# Gunicorn
GUNICORN_WORKERS = CPU_CORES * 2 + 1  # 一般是 c * 2 + 1
GUNICORN_THREADS = THREAD_NUM

GUNICORN_PORT = SERVER_PORT
GUNICORN_WORK_CLASS = "uvicorn.workers.UvicornWorker"
GUNICORN_MAX_REQUESTS = 1000
GUNICORN_LOGLEVEL = "WARNING"
GUNICORN_ERRORLOG = "./gunicorn.log"
GUNICORN_CAPTURE_OUTPUT = True

# MySQL
MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_POOL_SIZE = \
    "root", "123456", "127.0.0.1", 3306, "db", THREAD_NUM + 1

# Redis
# 一般不设置REDIS_POOL_SIZE
REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD = \
    "127.0.0.1", 6379, 2, "123456"

SECRET_KEY = "xxx"
