from project import db

class ShowGenre(db.Model):
    __tablename__ = 'show_genre'
    show_id = db.Column(db.String(50), db.ForeignKey('netflix.show_id'))
    genre_id = db.Column(db.Integer,db.ForeignKey('genres.genre_id'))
    __mapper_args__ = {
        "primary_key": [show_id,genre_id]
    }