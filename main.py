from orders.order_matching_engine import OrderMatchingEngine
from orders.order import Order
from orders.order import Side
from orders.order import OrderType

if __name__ == '__main__':
    engine = OrderMatchingEngine()

    order_s1 = Order(id=1, side=Side.SELL, price=100, quantity=10, trader='A')
    order_s2 = Order(id=2, side=Side.SELL, price=200, quantity=20, trader='B')
    order_s3 = Order(id=3, side=Side.SELL, price=300, quantity=50, trader='C')

    order_b1 = Order(id=4, side=Side.BUY, price=70, quantity=10, trader='D')
    order_b2 = Order(id=5, side=Side.BUY, price=300, quantity=20, trader='E', type=OrderType.MARKET)
    order_b3 = Order(id=6, side=Side.BUY, price=400, quantity=30, trader='F')

    engine.add_order(order_s1)
    engine.add_order(order_s2)
    engine.add_order(order_s3)

    engine.add_order(order_b1)
    engine.add_order(order_b2)
    engine.add_order(order_b3)

    engine.start()