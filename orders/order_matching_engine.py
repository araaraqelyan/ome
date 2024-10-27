import uuid

from orders.order import Order
from orders.order_book import OrderBook
from orders.status import Status
from orders.transaction import Transaction


class OrderMatchingEngine:

    def __init__(self):
        self.running = False
        self.order_book = OrderBook()
        self.transactions = []

    def add_order(self, order: Order):
        self.order_book.add_order(order)

    def remove_order(self, order: Order):
        success = self.order_book.remove_order(order)
        if not success:
            print("Invalid order.")

    def match_orders(self):
        if self.order_book.buy_orders and self.order_book.sell_orders:
            highest_buy_price, buy_order = self.order_book.buy_orders[0]
            lowest_sell_price, sell_order = self.order_book.sell_orders[0]

            if buy_order.status == Status.CANCEL:
                self.order_book.remove_order(buy_order)

            if sell_order.status == Status.CANCEL:
                self.order_book.remove_order(sell_order)

            # Check if the top buy and sell orders can be matched
            if self.order_book.matching_order_exists(buy_order) and self.order_book.matching_order_exists(sell_order):
                # Determine the trade quantity
                trade_quantity = min(buy_order.quantity, sell_order.quantity)

                # Log the transaction
                transaction = Transaction(
                    id = uuid.uuid4(),
                    buy_order = buy_order.id,
                    sell_order = sell_order.id,
                    buyer = buy_order.trader,
                    seller = sell_order.trader,
                    quantity = trade_quantity,
                    price = sell_order.price,
                )
                self.transactions.append(transaction)

                # Update quantities
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                # Remove orders if fully fulfilled
                if buy_order.quantity == 0:
                    self.order_book.remove_order(buy_order)
                if sell_order.quantity == 0:
                    self.order_book.remove_order(sell_order)

    def start(self):

        self.running = True
        try:
            while self.running:
                self.order_book.cleanup_expired_orders()

                self.match_orders()

                while self.transactions:
                    tx = self.transactions.pop()
                    print(f"Trade executed: {tx.buyer} buys {tx.quantity} from {tx.seller} at {tx.price}")

        except KeyboardInterrupt:
            print("Order matching engine stopped.")
            self.running = False

    def stop(self):
        self.running = False
        print("Order matching engine stopped.")