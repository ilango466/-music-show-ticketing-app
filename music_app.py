import os
import decimal
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    make_response,
    session,
    g,
    url_for,
)
import src.controllers.controller as ctrl
from src.models import event
from src.models import venue
from src.models.event import Event
from dotenv import load_dotenv
from src.db.connection_pool import get_connection
from src.db.database import Database
from src.models.ticket import Ticket
from src.models.user import User
from src.models.venue import Venue


load_dotenv()

app = Flask("Music-Show-Ticketing")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
app.config["SESSION_COOKIE_NAME"] = "ticket_thada"

#mail = Mail(app)

TAX = float(0.18)


@app.before_request
def before_request():
    g.email = None
    if "email" in session:
        g.email = session["email"]


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
def landing_page():
    return render_template("landing.html")


@app.route("/login")
def login_page():
    return render_template("login_signup_page.html", msg="")


@app.route("/verifyuser", methods=["POST"])
def verify_user():
    
    try: 
        user_mail = request.get_json()["email"]

        if user_mail != '':
            print(user_mail)
            msg, status = ctrl.is_user_exists(user_mail)
            return msg, status
    except KeyError as error:
        return {"msg": True, 'err': 'Invalid email...!'}, 200
    
@app.route("/addnewuser", methods=["POST"])
def add_new_user():
    sign_up_data = dict(request.form)
    ctrl.add_new_user(sign_up_data)
    return render_template("login_signup_page.html", msg="Sign up succesfull")
    


@app.route("/userlogout", methods=["GET"])
def logout():
    session.pop("email", None)
    return redirect(url_for("landing_page"))


@app.route("/userlogin", methods=["POST"])
def verify_login():
    login_credentials = dict(request.form)
    email = login_credentials["email"]
    password = login_credentials["password"]
    if ctrl.is_valid_user(email, password):
        session["email"] = email
        return redirect(url_for("user_page"))
    else:
        return render_template("login_signup_page.html", msg="Invalid User")


# ----  ADMIN -----


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/admin/addnewshow")
def add_show_page():
    venues = Venue.all()
    if venues:
        events = Event.all()
        events_data = [
            {"event": event, "venue": Venue.get_by_id(event.venue_id)}
            for event in events
        ]
        return render_template("add_show.html", events_data=events_data, venues=venues)
    return redirect(url_for("add_venue_page"))


@app.route("/admin/add_event", methods=["POST"])
def add_show_controller():
    data = dict(request.form)
    event_data = (
        data["event_name"],
        data["event_date"],
        data["event_from_date"],
        data["event_to_date"],
        data["event_price"],
        data["venue"],
        data["description"],
    )
    ctrl.add_new_event(event_data)
    return redirect(url_for("add_show_page"))


@app.route("/admin/update_event", methods=["POST"])
def update_event():
    event_id = int(request.args.get("id"))
    data = dict(request.form)
    event_data = (
        data["event_name"],
        data["event_date"],
        data["event_from_date"],
        data["event_to_date"],
        data["event_price"],
        data["venue"],
        data["description"],
    )
    ctrl.update_event(event_data, event_id)
    return redirect(url_for("add_show_page"))


@app.route("/admin/editshow", methods=["GET"])
def show_edit_page():
    event_id = int(request.args.get("id"))
    fetched_event = ctrl.get_event(event_id)
    return render_template(
        "show_edit_page.html",
        event=fetched_event,
        venues=Venue.all(),
        selected_venue=fetched_event.venue_id,
    )


@app.route("/admin/deleteshow/<int:event_id>", methods=["DELETE"])
def delete_show(event_id):
    ctrl.delete_event(event_id)
    return redirect(url_for("add_show_page"))


@app.route("/admin/addnewvenue", methods=["GET"])
def add_venue_page():
    return render_template("add_venue.html", venues=Venue.all())


@app.route("/admin/add_venue", methods=["POST"])
def add_new_venue():
    data = dict(request.form)
    event_data = (
        data["venue_name"],
        data["venue_adress"],
        data.get("platinum", None),
        data.get("gold", None),
        data.get("silver", None),
        data.get("bronze", None),
    )
    ctrl.add_new_venue(event_data)
    return redirect(url_for("add_venue_page"))


# ----  ADMIN END-----

# ----  USER -----


@app.route("/user")
def user_page():
    if g.email:
        return render_template("user_home.html", events=Event.all())
    return redirect(url_for("landing_page"))


@app.route("/user/seat_selection", methods=["GET"])
def seat_selection_page():
    if g.email:
        event_id = int(request.args.get("id"))
        booked_status = ctrl.get_booked_seats(event_id)

        return render_template(
            "seat_selection.html",
            booked_status=booked_status,
            event_id=event_id,
            isselected=False
        )
    else:
        return redirect(url_for("landing_page"))


@app.route("/user/seat_selected", methods=["POST"])
def seat_selected():
    if g.email:
        event_id = request.args.get("id")
        data = dict(request.form)
        print(data)
        selected_seat_info = ctrl.get_selected_seats_details(
            data["seat_type"], int(data["person_count"]), int(event_id)
        )
        booked_status = ctrl.get_booked_seats(event_id)
        temp_booked_seats = data["seat_type"]
        if booked_status[temp_booked_seats] >= int(data["person_count"]):
            return render_template(
                "seat_selection.html",
                person_count=data["person_count"],
                temp_booked_seats=temp_booked_seats,
                booked_status=booked_status,
                selected_seat_info=selected_seat_info,
                event_id=event_id,
                isselected=True,
                tax=TAX,
            )
        else:
            booked_status = ctrl.get_booked_seats(event_id)

            return render_template(
                "seat_selection.html",
                booked_status=booked_status,
                event_id=event_id,
                isselected=False,
                issoldout=True,
            )
        
        
    return redirect(url_for("landing_page"))


@app.route("/user/make_order", methods=["POST"])
def make_order():
    if g.email:
        data = request.get_json()
        message, status = ctrl.make_payment(data)
        return make_response(message, status)

    return redirect(url_for("landing_page"))


@app.route("/user/show_list")
def show_list_page():
    if g.email:
        all_events = Event.all()
        events = [[event, Venue.get_by_id(event.venue_id)] for event in all_events]
        return render_template("show_list.html", events=events)
    else:
        return render_template("login_signup_page.html", msg="Login First....!")


@app.route("/user/mybookings")
def my_bookings():
    if g.email:
        bookings = ctrl.get_my_bookings(User.get_user_by_mail(session["email"]).user_id)
        return render_template("mybookings.html", bookings=bookings)
    else:
        return render_template("login_signup_page.html", msg="Login First....!")


if __name__ == "__main__":
    with get_connection() as connection:
        Database.create_tables(connection)
    app.run(port=5000, debug=True)
