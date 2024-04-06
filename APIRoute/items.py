from typing import Union, List

from fastapi import APIRouter, Query

from ObjectModel import Item

items_route = APIRouter(prefix='/items', tags=["items"])


# 匹配规则与定义的顺序有关
@items_route.get('/all')
async def items_all():
    return [1, 2, 3, 4]


@items_route.get("/get_{item_id}")
# async def read_item(item_id: str, q: str | None = None):
async def get_item(item_id: str, q: Union[str, None] = None):
    # python3.10支持 类型 | 类型
    # python3.8需要写成 Union[str, None]
    # = None代表该参数可选
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# 通用匹配一般放在最后
@items_route.get('/{item_id}')
async def items(item_id: int):
    return item_id ** item_id


# 参数校验 可以使用regex
@items_route.post('/q')
async def read_items(
        q_list_int: List[int],
        q_list_str: List[str] = ("123", "abc"),
        q_str_required: str = Query(max_length=10, pattern=".*abc.*"),
        q_int: Union[int, None] = Query(default=None, ge=0, le=100),
        q_str: Union[str, None] = Query(default=None),
        q_alias: Union[str, None] = Query(None, alias="item-query")
):
    # 不带有Query的参数会从请求体中解析
    # 带有Query的参数会从请求路由? & &中解析
    # Query不添加default代表必填 请求体不添加=代表必填
    # List类型的不要设置default要设置成元组
    # Query的参数可以设置别名alias
    results = {
        "items": [{"item_id": "Foo"}, {"item:_id": "Bar"}]
    }
    results.update({"q_str_required": q_str_required})
    if q_list_str:
        results.update({"q_list_str": q_list_str})
    if q_list_int:
        results.update({"q_list_int": q_list_int})
    if q_alias:
        results.update({"q_alias": q_alias})
    if q_int:
        results.update({"q_int": q_int})
    if q_str:
        results.update({"q_str": q_str})
    print(results)
    return results


@items_route.post('/')
async def create_item(item: Item):
    # item称之为请求体 请求体一般采用数据模型进行接收
    # 函数中元类型的参数称之为请求参数
    # 路由中的{arg}称之为路径参数
    print(item)
    return item


