from fastapi import APIRouter

from ObjectModel import ModelName

models_route = APIRouter(prefix='/models', tags=["models"])


# 注意路由匹配顺序
@models_route.get('/find_{model_name}')
async def find_model_name(model_name: str, tt: int):
    # /models/find_123?model_name=456&tt=123
    # model_name会被解析为123
    return model_name, tt


@models_route.get('/{model_name}')
async def get_model_name(model_name: ModelName):
    # 限定路由访问要定义枚举类型
    # print(model_name == model_name.value)
    # print(model_name)  # 拿到枚举值
    # print(model_name.value)  # 拿到真实值

    if model_name is ModelName.lenet:
        return {'model_name': model_name, 'model_desc': 'lenet is good'}
    elif model_name is ModelName.alexnet:
        return {'model_name': model_name, 'model_desc': 'alexnet is good'}
    else:
        # 这里可以直接使用else引入路由如果不在枚举之中是访问不到这个函数体内的
        return {'model_name': model_name, 'model_desc': 'resnet is good'}
