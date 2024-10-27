import uuid
from dataclasses import dataclass


@dataclass(kw_only=True)
class Transaction:

    id: uuid.UUID
    buy_order: int
    sell_order: int
    buyer: str
    seller: str
    quantity: float
    price: float
