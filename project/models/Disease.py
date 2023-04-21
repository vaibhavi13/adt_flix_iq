from project import db

class Disease(db.Model):
    __tablename__ = 'disease'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True)