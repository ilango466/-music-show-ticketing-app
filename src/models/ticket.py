from src.db.connection_pool import get_connection
from src.db.database import Database


class Ticket:
    def __init__(self, event_id, price, seat_type, order_id, ticket_id=None):
        self.ticket_id = ticket_id
        self.event_id = event_id
        self.price = price
        self.seat_type = seat_type
        self.order_id = order_id

    def save(self):
        with get_connection() as connection:
            print((self.event_id, self.price, self.seat_type, self.order_id))
            ticket_id = Database().add_new_ticket(
                connection, (self.event_id, self.price, self.seat_type, self.order_id))
            if ticket_id:
                print(
                    f"Ticket for Event ID {self.event_id} saved with ID: {ticket_id}")

    @classmethod
    def all(cls, _id, by='event'):
        with get_connection() as connection:
            tickets = Database().get_all_tickets(connection, by=by, _id=_id)
            return [cls(ticket[1], ticket[2], ticket[3], ticket[4], ticket[0]) for ticket in tickets]

    def __repr__(self) -> str:
        return f"Ticket({self.ticket_id}, Event ID: {self.event_id})"
