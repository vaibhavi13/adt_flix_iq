from project import db

class Country(db.Model):
    __tablename__ = 'country'
    show_id = db.Column(db.String(50), db.ForeignKey('netflix.show_id'))
    country_name = db.Column(db.String(100))
    __mapper_args__ = {
        "primary_key": [show_id,country_name]
    }