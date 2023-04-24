from project import db

class Netflix(db.Model):
    __tablename__ = 'netflix'
    show_id = db.Column(db.String(50),primary_key=True)
    show_type = db.Column(db.String(20))
    title = db.Column(db.String(500))
    date_added = db.Column(db.Date)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    description = db.Column(db.String(1000))

