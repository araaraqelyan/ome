import datetime
from dataclasses import dataclass, field

from orders.order_type import OrderType
from orders.side import Side
from orders.status import Status

@dataclass(kw_only=True)
class Order:
    id: int
    side: Side
    price: float
    quantity: float
    trader: str
    timestamp: datetime.datetime | None = None

    status: Status = field(default=Status.OPEN)
    type: OrderType = field(default=OrderType.LIMIT)

    def __post_init__(self) -> None:
        if self.type == OrderType.MARKET:
            self.price = 0 if self.side == Side.SELL else float("inf")