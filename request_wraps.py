from functools import wraps
from fastapi import Request

def auth_require(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        # 如果不带有request参数，可以使用下面的方式获取
        # request = kwargs['request']

        # 注意async def
        print(request.headers)
        print(args, kwargs)
        print('something before func')
        print(f'{func.__name__} is called')
        # 注意return await
        return await func(request, *args, **kwargs)
    return wrapper