from src.db.connection_pool import get_connection
from src.db.database import Database
from datetime import datetime, time, timedelta


class Event:
    def __init__(self, event_name, event_date, event_from_time, event_to_time, event_price, venue_id, description, event_id=None):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_from_time = event_from_time
        self.event_to_time = event_to_time
        self.event_price = event_price
        self.venue_id = venue_id
        self.description = description
        my_time = str(event_from_time).split(':')
        self.door = (datetime.combine(datetime.today(), time(
            int(my_time[0]), int(my_time[1]))) - timedelta(hours=1)).time()

    def save(self):
        with get_connection() as connection:
            event_id = Database().add_new_event(self, connection=connection)
            if event_id is not None:
                self.event_id = event_id
                print(
                    f"Event :{self.event_name} saved with id : {self.event_id}")

    def update(self):
        with get_connection() as connection:
            update_status = Database().update_event(self, connection=connection)
            if update_status:
                print(f"Event :{self.event_name} Updated")
            else:
                print(f"Event :{self.event_name} not Updated")

    @staticmethod
    def delete(event_id):
        with get_connection() as connection:
            update_status = Database().delete_event(event_id, connection=connection)
            if update_status:
                print(f"Event :{event_id} Deteted")
            else:
                print(f"Event :{event_id} not Deteted")

    @classmethod
    def all(cls):
        with get_connection() as connection:
            events = Database().get_all_events(connection)
            return [cls(event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[0]) for event in events ]

    @classmethod
    def get_by_id(cls, event_id):
        with get_connection() as connection:
            event = Database().get_one_event(connection, int(event_id))
            return cls(event[1], event[2], event[3], event[4], event[5], event[6], event[7], event[0])

    def __repr__(self) -> str:
        return f"Event({self.event_id},{self.event_name})"
