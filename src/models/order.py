from src.db.connection_pool import get_connection
from src.db.database import Database

class Order:
    def __init__(self, user_id, event_id, quantity, total_amount, order_date, order_id=None):
        self.order_id = order_id
        self.user_id = user_id
        self.event_id = event_id
        self.quantity = quantity
        self.total_amount = total_amount
        self.order_date = order_date

    def save(self):
        with get_connection() as connection:
            order_id = Database().add_new_order(connection, (self.user_id, self.event_id, self.quantity, self.total_amount, self.order_date))
            if order_id:
                self.order_id = order_id
                print(f"Order ID {self.order_id} saved for User ID {self.user_id}")

    @classmethod
    def all(cls,user_id):
        with get_connection() as connection:
            orders = Database().get_all_orders(connection,user_id)
            return [cls(order[1], order[2], order[3], order[4], order[5], order[0]) for order in orders]

    def __repr__(self) -> str:
        return f"Order({self.order_id}, User ID: {self.user_id})"