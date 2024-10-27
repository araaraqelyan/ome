from datetime import datetime
from typing import List, Tuple
import heapq

from orders.order import Order
from orders.side import Side

class OrderBook:

    def __init__(self):
        self.buy_orders: List[Tuple[float, Order]] = [] # max-heap
        self.sell_orders: List[Tuple[float, Order]] = [] # min-heap
        self.timestamp = []

    def add_order(self, order: Order):
        if order.side == Side.BUY:
            heapq.heappush(self.buy_orders, (-order.price, order))
        else:
            heapq.heappush(self.sell_orders, (order.price, order))


    def remove_order(self, order: Order) -> bool:
        if order.side == Side.BUY:
            orders = self.buy_orders
        else:
            orders = self.sell_orders

        for i, (_, item) in enumerate(orders):
            if item.id == order.id:
                orders.pop(i)
                heapq.heapify(orders)
                return True
        return False

    def cleanup_expired_orders(self):
        current_time = datetime.now()

        self.buy_orders = [(price, order) for price, order in self.buy_orders if order.timestamp is None or order.timestamp > current_time]
        heapq.heapify(self.buy_orders)

        self.sell_orders = [(price, order) for price, order in self.sell_orders if order.timestamp is None or order.timestamp > current_time]
        heapq.heapify(self.sell_orders)

    def matching_order_exists(self, order: Order) -> bool:
        match order.side:
            case Side.SELL:
                return order.price <= self._max_buy()
            case Side.BUY:
                return order.price >= self._min_sell()


    def _max_buy(self) -> float:
        if len(self.buy_orders):
            return -self.buy_orders[0][0]
        return 0.0

    def _min_sell(self) -> float:
        if len(self.sell_orders):
            return self.sell_orders[0][0]
        return float("inf")
