from fastapi import FastAPI, Request, Header
from APIRoute import items_route, models_route, users_route
from ObjectModel.data import TimeDate

app = FastAPI(title="接口文档", version="1.0.0")


@app.get('/')
async def root(request: Request):
    print(request.client.host)
    return {'msg': 'Hello FastAPI'}

@app.post('/header_test')
async def header_test(request: Request, x_path: str = Header(), x_token: str = Header()):
    # Header和Query、Body是同类型的
    print(request.headers)
    print(x_path)
    print(x_token)
    return request.headers

@app.post('/time_test')
async def time_test(d: TimeDate):
    return {"date": d.date_, "time": d.time_,
            "datetime": d.datetime_, "timedelta": d.timedelta_}

# 可以接收bool值
@app.get('/bool_test')
async def bool_test(bool_value: bool = False):
    print(bool_value)
    # 1 yes on true True
    # 0 no off false False
    return bool_value

app.include_router(items_route)
app.include_router(models_route)
app.include_router(users_route)
