from project import db

class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    no_of_covid_beds = db.Column(db.Integer)
    doctor = db.relationship('Doctor', backref='Hospital')
