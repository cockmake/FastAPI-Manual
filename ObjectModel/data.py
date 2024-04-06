from typing import Union, Set
from datetime import datetime, date, timedelta, time
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    price: float
    tax: Union[float, None] = None
    description: Union[str, None] = None

    # 添加整个测试实例到文档中
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
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
    owner: User | None = None

class TimeDate(BaseModel):
    date_: date | None = Field(default=None, examples=["2024-04-07"])
    time_: time | None = Field(default=None, examples=["12:00:00"])
    datetime_: datetime | None = Field(default=None, examples=["2024-04-07 12:00:00"])
    # random valid timedelta
    timedelta_: timedelta | None = Field(default=None, examples=["1 days, 02:03:04"])