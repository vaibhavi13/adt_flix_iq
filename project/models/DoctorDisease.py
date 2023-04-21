from project import db

class DoctorDisease(db.Model):
    __tablename__ = 'doctor_disease'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))   
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))
    __mapper_args__ = {
        "primary_key": [doctor_id,disease_id]
    }
    