from datetime import time
import aiofiles
from datetime import time
import time as sys_time
import aiofiles
from fastapi import APIRouter, Form, UploadFile, Depends, Body, Request, BackgroundTasks
from starlette.responses import FileResponse
from redis import asyncio as aioredis
from dependencies import AccessTimeLimitDepend, AccessBeforeLimitDepend
from entity.data import User, Item
from curd import aio_redis_pool, aio_mysql_pool
from utils import generate_token, get_operation_description

users_route = APIRouter(prefix='/user', tags=["user"])


@users_route.post(
    '/create',
    response_model=User,
    # 也可以是基本类型 int str bool float Dict List
    # 也可以是某个类型的列表 List[User]
    # 也可以是多种类型 Union[User, Image, PlaneItem, CarItem]
    response_model_exclude_none=True,  # 不返回None值
    # response_model_exclude_unset=True,  # 不返回默认值 如果请求中有传入则返回
    response_model_exclude_defaults=True,  # 不返回默认值 如果传入了值与默认值相同也不返回
    response_model_exclude={"password"}
)
async def create_user(user: User):
    return user


@users_route.post(
    '/access_test',
    dependencies=[
        # 12:00:00前可以访问
        Depends(AccessBeforeLimitDepend(time(23, 0, 0))),
        # 访问次数限制含有权限检验了
        Depends(AccessTimeLimitDepend(5, 60))
    ]
)
async def user_access_test(item: Item = Body()):
    return {"msg": "success", "item": item}


@users_route.get('/image')
async def user_image():
    # 并且可以弹出下载框
    return FileResponse('a.jpg', media_type='image/jpg',
                        headers={'Content-Disposition': 'attachment; filename=a.jpg'})

@users_route.post('/upload/stream')
async def user_upload_stream(request: Request):
    # 流
    # 写入并返回该文件
    async with aiofiles.open('a.jpg', 'wb') as f:
        async for chunk in request.stream():
            await f.write(chunk)
    return FileResponse('a.jpg', media_type='image/jpg')


@users_route.post('/upload', summary="接收用户传入的文件和字段")
async def user_upload(file_a: UploadFile, username: str = Form(description="额外的字段")):
    """
    # 会以Markdown的形式显示在文档中

    ## 上传文件接口
    - **file_a**: 上传的文件
    - **username**: 其他字段
    """
    # 如果是多个文件可以使用List[UploadFile]来接收

    # 请求表单数据UploadFile Form类型的数据 Body Header Query是用一类型的数据
    # UploadFile 与 bytes 相比有更多优势
    # 存储在内存的文件超出最大上限时，FastAPI 会把文件存入磁盘；
    # 这种方式更适于处理图像、视频、二进制文件等大型文件，好处是不会占用所有内存；
    # 自带 file-like async 接口

    # 注意UploadFile中的方法为异步方法 在async def的函数中需要await def的函数正常使用即可
    # 异步写入文件 一次性写入2MB文件 需要aiofiles库
    step = 1024 * 1024 * 2
    async with aiofiles.open(file_a.filename, 'wb') as f:
        while content := await file_a.read(step):
            # 赋值运算符 := 用于给变量赋值，并且返回赋的值
            await f.write(content)
    # 在普通 def 路径操作函数 内，则可以直接访问 UploadFile.file 属性
    # 相当于同步写入文件
    # shutil.copyfileobj(file_a.file, open(file_a.filename, 'wb'))
    print(username)
    return username

async def write_file_task():
    async with aiofiles.open('a.txt', 'w') as f:
        for i in range(1000):
            await f.write('Hello FastAPI\n')
async def send_email_to():
    pass

@users_route.post('/write_file')
async def write_file(bk_task: BackgroundTasks):
    # 后台任务
    # 在请求需要使用的地方导入BackgroundTasks即可
    # 包括依赖项
    bk_task.add_task(write_file_task)
    return {"msg": "success"}

@users_route.post('/login')
async def user_login(username: str = Body(), password: str = Body()):
    user_info = await aio_mysql_pool.query_user_info_from_username(username)
    if not user_info:
        return {"msg": "用户名不存在或在审核中！", "type": "error"}
    password_db = user_info['password']
    if password != password_db:
        return {"msg": "密码错误！", "type": "error"}
    user_type = user_info['operation_type']
    day_access = 3
    cur_t = int(sys_time.time())
    time_to_live = day_access * 24 * 60 * 60
    token = generate_token(username, cur_t, time_to_live, user_type=user_type)
    name = user_info['name']
    # 把该用户的权限写入redis
    # 根据用户名查询权限
    privilege = await aio_mysql_pool.get_user_privilege(username, name)  # privilege 是 dict 包含了username name 权限
    async with aioredis.Redis(connection_pool=aio_redis_pool) as redis_op:
        # 以token为key 需要写入字段 用户名 姓名 *权限 操作类型
        # 最后设置过期时间
        await redis_op.hset(token, mapping=privilege)
        await redis_op.hset(token, "operation_type", user_type)
        await redis_op.expire(token, time_to_live)
    # 写入登录日志
    login_desc = get_operation_description(name, "登录", [])
    # 将信息登录日志写入数据库
    await aio_mysql_pool.write_operation_log(username, "登录", login_desc)
    return {"msg": "登录成功！", "type": "success", "access_token": token, "username": username,
            "name": name, "operation_type": user_type, 'privilege': privilege}
