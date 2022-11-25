from db import db
from flask_login import UserMixin
from sqlalchemy.sql import func

def getdb():
    return db


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256))
    user_name = db.Column(db.String(150))
    isowner = db.Column(db.Boolean)
    listroom = db.relationship('Listroom', backref='user')
    review = db.relationship('Reviews', backref='user')
    





# class Host(db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password1 = db.Column(db.String(150))
#     user_name = db.Column(db.String(150))
    


class Listroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    phone_no= db.Column(db.Integer)
    city = db.Column(db.String(150))
    host_name = db.Column(db.String(150))
    homestay_name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    description= db.Column(db.String(150))
    no_of_room = db.Column(db.Integer)
    Parking = db.Column(db.Boolean)
    Internet = db.Column(db.Boolean)
    Running_Hot_water = db.Column(db.Boolean)
    Open_Seating_areas = db.Column(db.Boolean)
    Air_Condition = db.Column(db.Boolean)
    Pet_Friendly = db.Column(db.Boolean)
    Toiletries = db.Column(db.Boolean)
    Smoking_Allowed = db.Column(db.Boolean)
    Library = db.Column(db.Boolean)
    Bonfire = db.Column(db.Boolean)
    Barbecue = db.Column(db.Boolean)
    Pick_and_dropService = db.Column(db.Boolean)
    rent=db.Column(db.Integer)
    pic=db.Column(db.String(500))
    uid = db.Column("uid", db.Integer, db.ForeignKey('user.id'))
    review = db.relationship('Reviews', backref='room')
    booking = db.relationship('Booking', backref='room')

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review=db.Column(db.String(5000))
    room_id = db.Column(db.Integer, db.ForeignKey('listroom.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
     

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_of_rooms= db.Column(db.Integer)
    no_of_guest= db.Column(db.Integer)
    contact_no= db.Column(db.Integer)
    date_ar=db.Column(db.DateTime)
    date_le=db.Column(db.DateTime)
    room_id = db.Column(db.Integer, db.ForeignKey('listroom.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    