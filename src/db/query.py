# event table

CRETATE_EVENT = """CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(255),
    event_date DATE,
    event_from_time TIME,
    event_to_time TIME,
    event_price DECIMAL(10,2),
    venue_id INT,
    description TEXT,
    FOREIGN KEY (venue_id) REFERENCES venues (venue_id)
);"""


INSERT_EVENT = """INSERT INTO events(
	 event_name, event_date, event_from_time, event_to_time, event_price, venue_id,description)
	VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING event_id;"""


UPDATE_EVENT = """UPDATE events
	SET  event_name=%s, event_date=%s, event_from_time=%s, event_to_time=%s, event_price=%s, venue_id=%s, description=%s
	WHERE event_id = %s RETURNING true;"""

DELETE_EVENT = """DELETE FROM events
	                WHERE event_id = %s RETURNING true;"""


SELECT_ONE_EVENT = "SELECT event_id, event_name, event_date, event_from_time, event_to_time,event_price, venue_id, description FROM events WHERE event_id = %s  ORDER BY event_id;;"

SELECT_ALL_EVENT = "SELECT event_id, event_name, event_date, event_from_time, event_to_time,event_price, venue_id, description FROM events ORDER BY event_id;"

# Venue Table

CREATE_VENUE = """CREATE TABLE IF NOT EXISTS venues (
    venue_id SERIAL PRIMARY KEY,
    venue_name VARCHAR(255),
    address VARCHAR(255)
);"""

VENUE_SEAT_TYPE = """CREATE TABLE IF NOT EXISTS seat_types (
    seat_type_id SERIAL PRIMARY KEY,
    seat_type_name VARCHAR(255),
    capacity INT,
    venue_id INT,
    FOREIGN KEY (venue_id) REFERENCES venues (venue_id) 
);"""


INSERT_VENUE = """INSERT INTO venues (venue_name, address)
                VALUES (%s, %s)
                RETURNING venue_id;
                """

INSERT_SEAT_TYPE = """INSERT INTO seat_types (seat_type_name, capacity, venue_id)
                VALUES (%s, %s, %s)
                RETURNING seat_type_id;
                """
SELECT_ONE_VENUE = """SELECT venue_id,
                        venue_name,
                        address,
                        MAX(platinum) AS platinum,
                        MAX(gold) AS gold,
                        MAX(silver) AS silver,
                        MAX(bronze) AS bronze from (SELECT v.*, 
                    (CASE WHEN s.seat_type_name = 'Platinum' THEN s.capacity end) AS Platinum,
                    (CASE WHEN s.seat_type_name = 'Gold' THEN s.capacity end) AS Gold,
                    (CASE WHEN s.seat_type_name = 'Silver' THEN s.capacity end) AS Silver,
                    (CASE WHEN s.seat_type_name = 'Bronze' THEN s.capacity end) AS Bronze
                    FROM venues v
                    JOIN seat_types s ON v.venue_id = s.venue_id) as a
                    GROUP BY venue_id, venue_name, address HAVING venue_id = %s ORDER BY a.venue_id;"""
                    
                    
SELECT_ALL_VENUES = """SELECT venue_id,
                        venue_name,
                        address,
                        MAX(platinum) AS platinum,
                        MAX(gold) AS gold,
                        MAX(silver) AS silver,
                        MAX(bronze) AS bronze from (SELECT v.*, 
                    (CASE WHEN s.seat_type_name = 'Platinum' THEN s.capacity end) AS Platinum,
                    (CASE WHEN s.seat_type_name = 'Gold' THEN s.capacity end) AS Gold,
                    (CASE WHEN s.seat_type_name = 'Silver' THEN s.capacity end) AS Silver,
                    (CASE WHEN s.seat_type_name = 'Bronze' THEN s.capacity end) AS Bronze
                    FROM venues v
                    JOIN seat_types s ON v.venue_id = s.venue_id) as a
                    GROUP BY venue_id, venue_name, address ORDER BY a.venue_id;"""

# Ticket Table

CREATE_TICKET = """CREATE TABLE IF NOT EXISTS tickets (
    ticket_id SERIAL PRIMARY KEY,
    event_id INT,
    price DECIMAL(10,2),
    seat_type VARCHAR(10),
    order_id INT,
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);
"""

INSERT_NEW_TICKET = """INSERT INTO tickets(
	 event_id, price, seat_type, order_id )
	VALUES (%s, %s, %s, %s) RETURNING ticket_id;"""

SELECT_ALL_TICKETS_BY_EVENT = "SELECT ticket_id, event_id, price, seat_type, order_id  FROM tickets WHERE event_id = %s;"

SELECT_ALL_TICKETS_BY_ORDER = "SELECT ticket_id, event_id, price, seat_type, order_id  FROM tickets WHERE event_id = %s;"

SELECT_ALL_TICKETS_BY_USER = "SELECT ticket_id, event_id, price, seat_type, order_id  FROM tickets WHERE order_id = %s;"


# User Table

CREATE_USER = """CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);
"""

INSERT_NEW_USER = """INSERT INTO users(
	 name, email, password )
	VALUES (%s, %s, %s) RETURNING user_id;"""


SELECT_ONE_USER_BY_MAIL = "SELECT user_id, name, email FROM users WHERE email = %s;"

CHECK_USER = "SELECT email FROM users WHERE email = %s AND password = %s;"

# User Order

CREATE_ORDER = """CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT,
    event_id INT,
    quantity INT,
    total_amount DECIMAL(10,2),
    order_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id)
);
"""

INSERT_NEW_ORDER = """INSERT INTO orders(
	 user_id, event_id, quantity, total_amount, order_date)
	VALUES (%s, %s, %s, %s, %s) RETURNING order_id;"""


SELECT_ALL_ORDERS = "SELECT order_id, user_id, event_id, quantity, total_amount, order_date  FROM orders WHERE user_id = %s "

# User Payment

CREATE_PAYMENT = """CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INT,
    amount DECIMAL(10,2),
    transaction_date DATE,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);
"""
