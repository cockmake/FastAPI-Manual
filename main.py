from datetime import datetime

from fastapi import FastAPI, Request, Header, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from dependencies import lifespan
from entity.data import TimeDate, Item
from routers import items_route, models_route, users_route

# dependencies=[] 可以设置全局依赖
# APIRouter同样可以设置


app = FastAPI(title="接口文档", version="1.0.0", redoc_url=None, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    '/',
    description="根路径",
    response_description="根路径返回值",
    deprecated=True
)
async def root(a: int = Query(default=0, ge=1)):
    # 有则检验，没有则默认值
    print(a)
    return {'msg': 'Hello FastAPI'}


@app.post('/header_test')
async def header_test(request: Request, x_path: str = Header(), x_token: str = Header()):
    # Header和Query、Body是同类型的
    print(request.headers)
    print(x_path)
    print(x_token)
    return request.headers


@app.get('/json_test')
async def json_test():
    # jsonable_encoder将数据模型转换为json可以接受的格式
    item = Item(name='Foo', price=35.4, tax=None, cur_t=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # item.dict() 将一个Pydantic数据模型转换为字典的时候也有类似的参数 exclude_xxxx
    # 但是不支持sqlalchemy_safe参数
    # 转换的是python数据类型 不是json数据类型 比如日期是datetime类型
    # .dict() 和 jsonable_encoder() 都是两种转换和筛选Pydantic数据模型的方法
    print(item.dict(
        exclude_none=True,
        exclude_defaults=True,
        exclude_unset=True
    ))
    # 写入数据库时使用jsonable_encoder
    return jsonable_encoder(
        [item, item],
        # exclude_none=True,
        # exclude_defaults=True,
        exclude_unset=True,
        sqlalchemy_safe=True
    )  # json-like


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
