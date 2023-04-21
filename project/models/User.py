from flask_login import UserMixin
from project import db


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    #curebox_user
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    #username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    #name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # FK added
    booking = db.relationship('Booking', backref='user')
    doctor = db.relationship('Doctor', backref='user')