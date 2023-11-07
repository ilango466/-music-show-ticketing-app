from src.db.connection_pool import get_cursor
import src.db.query as query


class Database:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_tables(connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.CREATE_VENUE)
            cursor.execute(query.VENUE_SEAT_TYPE)
            cursor.execute(query.CRETATE_EVENT)
            cursor.execute(query.CREATE_USER)
            cursor.execute(query.CREATE_ORDER)
            cursor.execute(query.CREATE_TICKET)

    # Adding New Event
    @staticmethod
    def add_new_event(event, connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_EVENT, (event.event_name, event.event_date,
                           event.event_from_time, event.event_to_time, event.event_price, event.venue_id, event.description))
            return cursor.fetchone()[0]

    @staticmethod
    def update_event(event, connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.UPDATE_EVENT, (event.event_name, event.event_date,event.event_from_time,event.event_to_time, event.event_price, event.venue_id, event.description,event.event_id))
            return cursor.fetchone()[0]

    @staticmethod
    def delete_event(event_id, connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.DELETE_EVENT, (event_id,))
            return cursor.fetchone()[0]

    @staticmethod
    def get_all_events(connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ALL_EVENT)
            return cursor.fetchall()

    @staticmethod
    def get_one_event(connection, event_id):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ONE_EVENT, (event_id,))
            return cursor.fetchone()

    #  --------- VENUE ----------
    
    @staticmethod
    def add_new_venue(*venue, connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_VENUE,venue)
            return cursor.fetchone()[0]
    
    @staticmethod
    def add_new_seat_type(*args, connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_SEAT_TYPE,(args))
            return cursor.fetchone()[0]
                
     

    @staticmethod
    def get_one_venue(connection, venue_id):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ONE_VENUE, (venue_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all_venues(connection):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ALL_VENUES)
            return cursor.fetchall()


    #  --- USER ---

    @staticmethod
    def add_new_user(connection, new_user):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_NEW_USER, new_user)
            return cursor.fetchone()[0]

    @staticmethod
    def get_one_user_by_mail(connection, user_email):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ONE_USER_BY_MAIL, (user_email,))
            user = cursor.fetchone()
            return user

    @staticmethod
    def check_user(connection, email, password):
        with get_cursor(connection) as cursor:
            cursor.execute(query.CHECK_USER, (email, password))
            return cursor.fetchone()

    # ---- ORDERS ----

    @staticmethod
    def add_new_order(connection, new_order):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_NEW_ORDER, new_order)
            return cursor.fetchone()[0]
        
        
    @staticmethod
    def get_all_orders(connection, user_id):
        with get_cursor(connection) as cursor:
            cursor.execute(query.SELECT_ALL_ORDERS, (user_id,))
            return cursor.fetchall()

    # ---- TICKETS ----

    @staticmethod
    def add_new_ticket(connection, new_ticket):
        with get_cursor(connection) as cursor:
            cursor.execute(query.INSERT_NEW_TICKET, new_ticket)
            return cursor.fetchone()[0]
        
    @staticmethod
    def get_all_tickets(connection, by='event', _id=None):
        query_map = {'event': query.SELECT_ALL_TICKETS_BY_EVENT, 'order':query.SELECT_ALL_TICKETS_BY_ORDER, 'user': query.SELECT_ALL_TICKETS_BY_USER}
        with get_cursor(connection) as cursor:
            cursor.execute(query_map[by],(_id,))
            return cursor.fetchall()
