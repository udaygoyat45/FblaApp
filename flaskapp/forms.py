from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=10, max=120)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is taken, please choose another")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken, please choose another")


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Log In')


class RedeemPoints(FlaskForm):
    flight_id = StringField("Your Frequent Flyer ID",
                            validators=[DataRequired()])
    submit = SubmitField("Redeem")


class AccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email(), Length(max=120)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=10, max=120)])
    submit = SubmitField("Apply")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account registered with this email")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=10, max=120)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")


class FlightOptions(FlaskForm):
    date = SelectField("Date")
    children_passengars = SelectField(
        "Minors", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    adult_passengars = SelectField(
        "Adults", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    flight_id = 0
    submit = SubmitField("Book My Flight")

class EditFlightOptions(FlaskForm):
    date = SelectField("Date")
    children_passengars = SelectField(
        "Minors", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    adult_passengars = SelectField(
        "Adults", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    flight_id = 0
    destroy = SubmitField("Erase this Booking")
    submit = SubmitField("Edit My Flight")

class SearchFlights(FlaskForm):
    from_location = SelectField("From Location")
    to_location = SelectField("To Location")

    submit = SubmitField("Filter")