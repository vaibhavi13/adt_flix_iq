from project import db

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer,primary_key=True)
    genre = db.Column(db.String(255))
    
