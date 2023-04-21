from project import db

class InsuranceProvider(db.Model):
    __tablename__ = 'InsuranceProvider'
    id = db.Column(db.Integer,primary_key=True)
    package_name = db.Column(db.String(255))
    package_description = db.Column(db.String(255))
    insurance_duration = db.Column(db.Integer)
    age = db.Column(db.String(255))
    price = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
    people_enrolled = db.Column(db.Integer)

