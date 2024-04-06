from functools import wraps
from fastapi import Request

def auth_require(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # 注意async def
        print(request.headers)
        print(args, kwargs)
        print('something before func')
        print(f'{func.__name__} is called')
        # 注意return await
        return await func(request, *args, **kwargs)
    return wrapper