from src.db.connection_pool import get_connection
from src.db.database import Database


class SeatType:
    def __init__(self, seat_type_name, capacity, venue_id, seat_type_id=None):
        self.seat_type_id = seat_type_id
        self.seat_type_name = seat_type_name
        self.capacity = capacity
        self.venue_id = venue_id

    def save(self):
        with get_connection() as connection:
            seat_type_id = Database().add_new_seat_type(
                self.seat_type_name, self.capacity, self.venue_id, connection=connection)
            if seat_type_id:
                print(
                    f"Seat type '{self.seat_type_name}' saved with ID: {seat_type_id}")

    @classmethod
    def all(cls):
        with get_connection() as connection:
            seat_types = Database().get_all_seat_types(connection)
            return [cls(seat_type[1], seat_type[2], seat_type[3], seat_type[0]) for seat_type in seat_types]

    def __repr__(self) -> str:
        return f"SeatType({self.seat_type_id}, '{self.seat_type_name}', {self.capacity}, {self.venue_id})"
