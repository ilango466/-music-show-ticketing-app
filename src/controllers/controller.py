from datetime import date
from flask import session
from src.services.mail_service import send_mail
from src.models.event import Event
from src.models.venue import Venue
from src.models.order import Order
from src.models.ticket import Ticket
from src.models.user import User

TAX = float(0.18)


def add_new_user(user_data):
    event = User(user_data["name"], user_data["email"], user_data["password"])
    event.save()


def get_event(event_id):
    return Event.get_by_id(event_id)


def is_valid_user(email, password):
    user = User.is_exists(email, password)
    return user


def get_selected_seats_details(seat_type,person_count, event_id):
    event = Event.get_by_id(event_id)
    venue = Venue.get_by_id(event.event_id)
    basic_price = float(event.event_price)
    price_catogory = {'Platinum': 0, 'Gold': 0.1,
                      'Silver': 0.2, 'Bronze': 0.4}
    catogarized_price = basic_price - (basic_price * float(price_catogory[seat_type])) 
    total_price = float(catogarized_price * person_count)
    return dict(count=person_count, price=catogarized_price, total_price=total_price, venue=venue, event=event)


def get_booked_seats(event_id):
    tickets = Ticket.all(event_id)
    venue = Venue.get_by_id(Event.get_by_id(event_id).venue_id)
    if tickets is not None:
        booked_seats_details = {'Bronze': venue.bronze,
                                'Silver': venue.silver, 'Gold': venue.gold, 'Platinum': venue.platinum}
        
        for ticket in tickets:
            if booked_seats_details[ticket.seat_type] is not None:
                booked_seats_details[ticket.seat_type] -= 1
                
        return booked_seats_details
    return None


def make_payment(payment_data):
    seat_details = get_selected_seats_details(
        payment_data["selected_seats"],int( payment_data["person_count"]), payment_data["event_id"]
    )
    event_id = int(payment_data["event_id"])
    event = Event.get_by_id(event_id)
    selected_seats = payment_data["selected_seats"]
    booked_seats = get_booked_seats(event_id)
    count = seat_details["count"]
    isavailable = booked_seats[selected_seats] >= (booked_seats[selected_seats] - count)
    tk_price = seat_details["price"]
    total_price = round(((tk_price * count) * TAX) + (tk_price * count), 2)
    if isavailable:
        user = User.get_user_by_mail(session["email"])
        date_of_order = date.today()
        print(total_price, date_of_order)
        order = Order(user.user_id, event_id, count,
                      total_price, date_of_order)
        order.save()
        print(order)
        for _ in range(count):
            Ticket(event_id, tk_price, selected_seats, order.order_id).save()
        send_mail(
            subject="Seat booking Confirmation",
            body=f"""Dear {user.name},

We are pleased to inform you that your booking for the show on {event.event_date} has been successfully processed. Your seat(s) have been reserved with the following details:

Show Name: {event.event_name}
Date: {event.event_date}
Seat type: {selected_seats}
Person Count:{count}""",
            reciever=user.email,
        )

        return ({"msg": "Booking Success", "success": True}, 200)
    else:
        return ({"msg": "Tickets sold out...!", "success": False}, 200)


def is_user_exists(user_email):
    user = User.get_user_by_mail(user_email)
    if user is None:
        return ({"msg": False}, 202)
    return ({"msg": True, 'err':'User already exists..!'}, 200)


def get_venue_by_id(venue_id):
    venue = Venue.get_by_id(venue_id)
    return venue


# ----------------------------------------
#           ADMIN
# ----------------------------------------


def add_new_event(event_details):
    event = Event(*event_details)
    event.save()


def update_event(event_data, event_id):
    event = Event(*event_data, event_id=event_id)
    event.update()


def delete_event(event_id):
    Event.delete(event_id)


def add_new_venue(venue_details):
    event = Venue(*venue_details)
    event.save()


#------------------------------------
#            USER
#------------------------------------

def get_my_bookings(user_id):
    all_orders = Order.all(user_id)
    print(all_orders)
    
    bookings = []
    for _order in all_orders:
        event = Event.get_by_id(_order.event_id)
        venue = Venue.get_by_id(event.venue_id)
        tickets = Ticket.all(_order.order_id, by='order')
        bookings.append({'event': event, 'venue': venue, 'tickets': tickets})
               
    return bookings