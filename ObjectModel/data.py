from pydantic import BaseModel
from typing import Union

class Item(BaseModel):
    name: str
    price: float
    tax: Union[float, None] = None
    description: Union[str, None] = None
