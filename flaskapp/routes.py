from flask import request, redirect, render_template, url_for, flash
from flaskapp.models import User, Flight, UserFlight, Message
from flaskapp import db, bcrypt, app, mail
from flaskapp.forms import (
    LoginForm,
    RegistrationForm,
    AccountForm,
    RequestResetForm,
    ResetPasswordForm,
    FlightOptions,
    EditFlightOptions,
    SearchFlights,
    MessageForm,
    NewsletterForm
)
import datetime
from flask_login import login_user, current_user, logout_user, login_required
import os
from flask import send_from_directory

# from ast import literal_eval
from flaskapp.generate import (
    generate_id,
    generate_registration_message,
    generate_reset_message,
    nice_colors,
    generate_flight_transcript
)


def set_up_choices():
    airports = set()
    for flight in Flight.query.all():
        airports.add(flight.from_location)

    final = []
    for airport in airports:
        final.append((airport, airport))

    return final


@app.route("/favicon.ico")
def favicon():
    print(app.root_path)
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchFlights()
    form.from_location.choices = set_up_choices()
    form.to_location.choices = set_up_choices()

    if form.validate_on_submit():
        print("did this just not run?")
        from_location = form.from_location.data
        to_location = form.to_location.data
        ffp = form.frequent.data
        refundable = form.refundable.data

        flight = Flight.query.filter_by(from_location=from_location, to_location=to_location).first()
        
        if flight == None:
            flash("A flight between these two airports doesn't exist currently. We are very sorry for any inconvenience.", "danger")
        else:
            print(type(flight.id))
            return redirect(url_for("final", id=flight.id))

    return render_template("home.html", form=form, extra=True, head=True, title="Gooday Airlines", animation=True, subtitle="Flights that make you dream.")


@app.route("/frequent", methods=['GET', 'POST'])
def frequent():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()

        flash("Your message was successfully delivered", 'success')
    
    return render_template("frequent.html", title="Frequent Flyer Program", form=form, user=current_user)


@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    form = SearchFlights()
    form.from_location.choices = set_up_choices()
    form.to_location.choices = set_up_choices()

    flights = None

    if form.validate_on_submit():
        print("did this just not run?")
        from_location = form.from_location.data
        to_location = form.to_location.data
        ffp = form.frequent.data
        refundable = form.refundable.data

        flight = Flight.query.filter_by(from_location=from_location, to_location=to_location).first()
        
        if flight == None:
            flash("A flight between these two airports doesn't exist currently. We are very sorry for any inconvenience.", "danger")
        else:
            return redirect(url_for("final", id=flight.id))

    flights = Flight.query.all()
    return render_template(
        "book.html",
        title="Book A Flight",
        flights=flights,
        form=form,
        nice_colors=nice_colors
    )


@app.route("/credits", methods=['GET', 'POST'])
def credits():
    form = MessageForm();
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()

        flash("Your message was successfully delivered", 'success')
        
        
    return render_template("credits.html", title="Credits", form=form)


@app.route("/job", methods=['GET', 'POST'])
def job():
    form = MessageForm();
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()

        flash("Your message was successfully delivered", 'success')
        
    return render_template("job.html", title="Jobs Available", form=form)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    user = current_user
    if form.validate_on_submit():

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if form.username.data != "":
                user.username = form.username.data
            if form.email.data != "":
                user.email = form.email.data

            db.session.commit()
            flash("Change Successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Change Unccessful. Please check password", "danger")
    return render_template(
        "account.html",
        title="Your Account",
        form=form,
        user=user,
        head=False,
        forms=True,
        image="../static/img/plane.jpg",
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode("utf-8")
        )
        new_flyer_id = generate_id(10)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            flyer_id=new_flyer_id,
        )
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login 👍", "success")

        generate_registration_message(
            form.username.data, form.email.data, new_flyer_id, mail, app
        )

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form,
        head=False,
        forms=True,
        title="Register",
        image="../static/img/plane.jpg",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
            user.password.decode('utf-8'), form.password.data
        ):
            flash("Login Successful. Welcome 😄", "success")
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unccessful. Please check username and password", "danger")
    return render_template(
        "login.html",
        name="login",
        head=False,
        form=form,
        forms=True,
        title="Login",
        image="../static/img/plane.jpg",
    )


@app.route("/final", methods=["GET", "POST"])
@login_required
def final():
    form = FlightOptions()
    flight_id = int(request.args.get("id"))
    flight = Flight.query.get(flight_id)

    curr = flight.date
    form.date.choices = []
    form.date.choices.append(
        (curr.strftime("%m/%d/%Y %S%M%H"), curr.strftime("%M/%d/%Y"))
    )

    for i in range(7):
        curr += datetime.timedelta(days=7)
        print(curr)
        form.date.choices.append(
            (curr.strftime("%m/%d/%Y %S%M%H"), curr.strftime("%M/%d/%Y"))
        )

    form.flight_id = flight_id

    if form.validate_on_submit():
        curr = UserFlight(
            date=datetime.datetime.strptime(form.date.data, "%m/%d/%Y %S%M%H"),
            user_id=current_user.id,
            flight_id=form.flight_id,
            children=int(form.children_passengars.data),
            adults=int(form.adult_passengars.data),
        )

        db.session.add(curr)
        db.session.add(flight)
        db.session.commit()

        flash("Your flight booking was successful. An email was sent to your account with details", "success")
        generate_flight_transcript(curr, Flight.query.filter_by(id=flight_id).first(), current_user.email, mail, app)
        return redirect(url_for("home"))

    return render_template(
        "final.html",
        flight=flight,
        name="Your Flight",
        head=True,
        title="Your Flight",
        forms=False,
        form=form,
    )


def send_reset_email(user):
    token = user.get_reset_token()
    generate_reset_message(user.username, user.email, token, mail, app)


@app.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        logout_user()
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to you ✔", "success")
        return redirect(url_for("login"))
    return render_template(
        "reset_request.html",
        name="Reset Password",
        head=False,
        form=form,
        forms=True,
        title="Reset Password",
        image="../static/img/plane.jpg",
    )


@app.route("/reset_token/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash(
            "That is an invalid or expired token. Are you a hacker? Or just clicked on wrong link 🤔",
            "warning",
        )
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode("utf-8")
        )
        user.password = hashed_password
        db.session.commit()

        flash("Your password has been updated 👍", "success")
        return redirect(url_for("login"))
    return render_template(
        "reset_token.html",
        name="Reset Password",
        head=False,
        form=form,
        forms=True,
        title="Reset Password",
        image="../static/img/plane.jpg",
    )


@app.route("/view")
@login_required
def view():
    all_flights = UserFlight.query.filter_by(user_id=current_user.id).all()
    flights_info = []
    for each in all_flights:
        flights_info.append(Flight.query.get(each.flight_id))
    return render_template(
        "view.html",
        flights=all_flights,
        flights_info=flights_info,
        title="View Your Booked Flights",
        nice_colors=nice_colors,
    )


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditFlightOptions()
    userflight_id = int(request.args.get("id"))
    the_flight = UserFlight.query.get(userflight_id)
    flight_id = int(request.args.get("id"))
    flight = Flight.query.get(flight_id)

    curr = flight.date
    form.date.choices = []
    form.date.choices.append(
        (curr.strftime("%m/%d/%Y %S%M%H"), curr.strftime("%M/%d/%Y"))
    )

    for i in range(7):
        curr += datetime.timedelta(days=7)
        form.date.choices.append(
            (curr.strftime("%m/%d/%Y %S%M%H"), curr.strftime("%M/%d/%Y"))
        )

    if form.validate_on_submit():
        if form.destroy.data:
            db.session.delete(the_flight)
            db.session.commit()

            return redirect(url_for("view"))
        else:
            the_flight.date = datetime.datetime.strptime(
                form.date.data, "%m/%d/%Y %S%M%H"
            )
            the_flight.children = int(form.children_passengars.data)
            the_flight.adults = int(form.adult_passengars.data)

            db.session.commit()

            return redirect(url_for("view"))

    return render_template(
        "edit.html",
        flight=flight,
        name="Your Booking",
        head=True,
        title="Your Booking",
        forms=False,
        form=form,
    )

@app.route("/about", methods=['GET', 'POST'])
def about():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()

        flash("Your message was successfully delivered", 'success')

    return render_template("about.html", form=form, title="About Gooday")