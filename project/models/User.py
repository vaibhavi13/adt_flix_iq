from flask_login import UserMixin
from project import db


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))