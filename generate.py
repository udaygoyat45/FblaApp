from flaskapp import db, bcrypt
from flaskapp.models import Flight, User
import datetime
import random

db.drop_all()
db.create_all()

uday = User(username="udaygoyat45", email="udaygoyat45@gmail.com", password=bcrypt.generate_password_hash(
            "udaygoyat#4".encode('utf-8')), points=0)

db.session.add(uday)
db.session.commit()

outfile = open("out.out", "w+")
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
            temp = Flight(from_location=airports[i], to_location=airports[j], date=datetime.datetime.now()+datetime.timedelta(days=random.randint(1, 6)), price=random.randint(300, 500), total=0)
            db.session.add(temp)
            db.session.commit()

