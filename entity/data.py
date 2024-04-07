from typing import Union, Set
from datetime import datetime, date, timedelta, time
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    price: float
    tax: Union[float, None] = None
    description: Union[str, None] = None
    # 这样写 时间是固定的 不是动态的
    # 要在实例化的时候进行修改
    cur_t: Union[datetime, None] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 添加整个测试实例到文档中
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                    "cur_t": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }
    }



class User(BaseModel):
    # 模型的字段校验 别忘记可以采用regex
    username: str = Field(min_length=2, examples=["make"])
    # examples会添加到文档中，方便直接测试和展示
    # 有默认值代表是可选的传入数值
    password: str = Field(default='', min_length=6, max_length=30, examples=["123456"])
    full_name: str = Field(default='', max_length=30)
    tags: Set[str] = Field(min_length=2, examples=[["string", "str"]])


# 模型嵌套
class Image(BaseModel):
    filename: str
    file_type: str = Field(default='jpg')
    owner: Union[User, None] = None

class TimeDate(BaseModel):
    date_: Union[date, None] = Field(default=None, examples=["2024-04-07"])
    time_: Union[time, None] = Field(default=None, examples=["12:00:00"])
    datetime_: Union[datetime, None] = Field(default=None, examples=["2024-04-07 12:00:00"])
    # random valid timedelta
    timedelta_: Union[timedelta, None] = Field(default=None, examples=["1 days, 02:03:04"])

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    size: int
    type: str = "plane"
