from flaskapp import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    flyer_id = db.Column(db.String(10), default=None)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class UserFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    adults = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Flight('{self.flight_id}', '{self.user_id}', '{self.date}', '{self.children}', '{self.adults}')"


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_location = db.Column(db.String(20), unique=False, nullable=False)
    to_location = db.Column(db.String(20), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False) #remember to delete this and fix any bugs
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Flight('{self.from_location}', '{self.to_location}', '{self.date}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.Integer(), unique=False, nullable=False)
    message = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return f'''Mesage(name: {self.name}, email: {self.email},
                        phone: {str(self.phone)}, message: {self.message})'''
