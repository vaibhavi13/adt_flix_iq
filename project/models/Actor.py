from project import db

class Actor(db.Model):
    __tablename__ = 'actor'
    show_id = db.Column(db.String(50), db.ForeignKey('netflix.show_id'))
    actor_name = db.Column(db.String(1000))
    __mapper_args__ = {
        "primary_key": [show_id,actor_name]
    }