from typing import Union, List
from pydantic import BaseModel


class Order(BaseModel):
    user_id: int
    shipping_address_id: Union[int, None] = None
    order_lines: List = [
        {
            'product_id': int,
            'sku': Union[str, None],
            'quantity': int,
        },
    ]
