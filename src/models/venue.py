from src.db.connection_pool import get_connection
from src.db.database import Database
from src.models.seat_type import SeatType


class Venue:
    def __init__(self, venue_name, address,platinum, gold, silver, bronze, venue_id=None):
        self.venue_id = venue_id
        self.venue_name = venue_name
        self.address = address
        self.platinum = platinum
        self.gold = gold
        self.silver = silver
        self.bronze = bronze
        self.total_capacity = sum(
            int(x) for x in [self.platinum, self.gold, self.silver, self.bronze] if x is not None)

    def save(self):
        with get_connection() as connection:
            venue_id = Database().add_new_venue(
                self.venue_name, self.address,connection=connection)
            if venue_id:
                self.venue_id = venue_id
                seat_types = {'Platinum': self.platinum, 'Gold': self.gold,
                              'Silver': self.silver, 'Bronze': self.bronze}
                for key in seat_types:
                    if seat_types[key] is not None:
                        SeatType(key, seat_types[key], self.venue_id).save()
                print(f"Venue '{self.venue_name}' saved with ID: {venue_id}")
    
    @classmethod
    def get_by_id(cls, venue_id):
        with get_connection() as connection:
            venue = Database().get_one_venue(connection, int(venue_id))
            return cls(venue[1], venue[2], venue[3], venue[4], venue[5], venue[6], venue[0])


    @classmethod
    def all(cls):
        with get_connection() as connection:
            venues = Database().get_all_venues(connection)
            return [cls(venue[1], venue[2], venue[3], venue[4], venue[5], venue[6], venue[0]) for venue in venues]

    def __repr__(self) -> str:
        return f"Venue({self.venue_id}, '{self.venue_name}')"
