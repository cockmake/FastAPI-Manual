# gunicorn -c gunicorn_conf.py main:app -D
from settings import (GUNICORN_WORKERS, GUNICORN_THREADS, GUNICORN_PORT, GUNICORN_WORK_CLASS, GUNICORN_MAX_REQUESTS,
                      GUNICORN_LOGLEVEL, GUNICORN_CAPTURE_OUTPUT, GUNICORN_ERRORLOG)

workers = GUNICORN_WORKERS
worker_class = GUNICORN_WORK_CLASS  # FastAPI部署采用 "uvicorn.workers.UvicornWorker"

threads = GUNICORN_THREADS

bind = f'0.0.0.0:{GUNICORN_PORT}'

max_requests = GUNICORN_MAX_REQUESTS
loglevel = GUNICORN_LOGLEVEL
capture_output = GUNICORN_CAPTURE_OUTPUT  # 标准输出和标准错误都重定向到错误日志文件中。
errorlog = GUNICORN_ERRORLOG
