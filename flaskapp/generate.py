from flask_mail import Message
from flask import url_for

def generate_id(N):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                                string.digits)
                   for _ in range(N))


def generate_registration_message(username, email, id, mail, app):
    msg = Message("Welcome to Gooday Airlines", recipients=[email])
    msg.body = f'''Hello, {username}
    Thank you for registering to Gooday Airlines. I hope you enjoy our service in the future.
    Your Frequent Flyer ID is {id}. Please save this ID somwhere since you would use
    this everytime you redeem your points. '''

    with app.open_resource("static/img/logo2.png") as fp:
        msg.attach("image.png", "image/png", fp.read())

    mail.send(msg)


def generate_reset_message(username, email, token, mail, app):
    msg = Message("Password Reset Request", recipients=[email])
    msg.body = f"""To reset your password, click on this link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request, don't worry you are safe 😁"""

    with app.open_resource("static/img/logo2.png") as fp:
        msg.attach("image.png", "image/png", fp.read())

    mail.send(msg)

def generate_flight_transcript (user_flight, flight, email, mail, app):
    msg = Message("Your Flight Booking", recipients=[email])
    msg.body = f"""Thank you for booking your flight with Gooday Airlines.
    You can change/cancel your booking by clicking on this link: {url_for('view')}

    From: {flight.from_location}
    To: {flight.to_location}
    Price: ${flight.price}
    Adults: {user_flight.adults}
    Minors: {user_flight.children}
    Date: {user_flight.date}
    """

    with app.open_resource("static/img/logo2.png") as fp:
        msg.attach("image.png", "image/png", fp.read())

    mail.send(msg)

nice_colors = [
    "rgb(241,67,87)",
    "rgb(83,162,227)",
    "rgb(244,173,73)",
    "rgb(103,87,226)",
    "rgb(105,222,146)",
    "rgb(241,60,31)",
    "rgb(68,49,141)",
]