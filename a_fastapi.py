from fastapi import FastAPI, Request
from APIRoute import items_route, models_route
app = FastAPI(title="接口文档", version="1.0.0")


@app.get('/')
async def root(request: Request):
    print(request.client.host)
    return {'msg': 'Hello FastAPI'}


# 可以接收bool值
@app.get('/bool_test')
async def bool_test(bool_value: bool = False):
    print(bool_value)
    # 1 yes on true True
    # 0 no off false False
    return bool_value

app.include_router(items_route)
app.include_router(models_route)
