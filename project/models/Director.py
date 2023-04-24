from project import db

class Director(db.Model):
    __tablename__ = 'director'
    show_id = db.Column(db.String(50), db.ForeignKey('netflix.show_id'))
    director_name = db.Column(db.String(100))
    __mapper_args__ = {
        "primary_key": [show_id,director_name]
    }