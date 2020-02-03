from flaskapp import db, bcrypt, mail
from flaskapp.models import Flight, User
from flaskapp.generate import generate_id, generate_message
import datetime
import random

db.drop_all()
db.create_all()

new_flyer_id = generate_id(10)
user = User(username="UdayGoyat",
            email="udaygoyat45@gmail.com", password=bcrypt.generate_password_hash(
                "udaygoyat#4".encode('utf-8')), flyer_id=new_flyer_id)

# generate_message("UdayGoyat", "udaygoyat45@gmail.com", new_flyer_id, mail, app)

db.session.add(user)
db.session.commit()


airports = ["Birmingham-Shuttlesworth International Airport (BHM)",
            "Huntsville International Airport (HSV)",
            "Addison Municipal Airport",
            "Hartsfield-Jackson Atlanta International Airport (ATL)",
            "Augusta Regional Airport (AGS)",
            "Brunswick Golden Isles Airport (BQK)",
            "Columbus Metropolitan Airport (CSG)"]

for i in range(len(airports)):
    for j in range(len(airports)):
        if (i != j):
            temp = Flight(from_location=airports[i], to_location=airports[j], date=datetime.datetime.now(
            )+datetime.timedelta(days=random.randint(1, 6)), price=random.randint(300, 500))
            db.session.add(temp)
            db.session.commit()
