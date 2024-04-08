from contextlib import asynccontextmanager
from datetime import datetime, time
from typing import Tuple

from fastapi import Header, HTTPException, Depends, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("初始化进程")
    yield  # 在该上下文环境下进入下一个步骤
    print("关闭进程")


# 不需要传入参数就用函数依赖即可
async def auth_require_depend(access_token: str = Header(), x_real_ip: str = Header()):
    print("检查权限")
    access_token = access_token.split(' ')[1]
    if access_token != "123":
        raise HTTPException(status_code=400, detail="Access-Token header invalid")
    username = "make"
    print("before auth_require_depend yield")
    yield username, x_real_ip, access_token
    print("after auth_require_depend yield")
    # return username, x_real_ip, access_token

    # yield username
    # yield会产生一个上下文
    # yield合适下一个函数也用到了这个上下文 例如数据库操作
    # 在完成后执行一些额外步骤的依赖项 例如关闭数据库连接


# 需要传入参数就用类依赖
class AccessTimeLimitDepend:
    def __init__(self, access_limit: int, time_limit: int):
        self.access_limit = access_limit
        self.time_limit = time_limit

    async def __call__(self, access_info: Tuple[str, str, str] = Depends(auth_require_depend)):
        print("检查访问次数")
        # 依赖项的参数是上一个依赖项的返回值 子依赖项的参数是父依赖项的返回值
        username, x_real_ip, access_token = access_info
        print("before AccessTimeLimit")
        print(f"username: {username}, x_real_ip: {x_real_ip}, access_token: {access_token}")
        print("after AccessTimeLimit")


# 限制访问时间段

class AccessBeforeLimitDepend:
    def __init__(self, access_time: time):
        self.access_time = access_time

    async def __call__(self):
        print("检查访问时间")
        cur_t = datetime.now().time()
        if cur_t > self.access_time:
            raise HTTPException(status_code=400, detail="Access time limit")
