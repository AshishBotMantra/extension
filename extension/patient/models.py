from extension import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    sex = db.Column(db.String())
    mobile_no = db.Column(db.Integer())
    time = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Integer())

    def __init__(self,name,age,sex,mobile_no,weight):
        self.name = name
        self.age = age
        self.sex = sex
        self.mobile_no = mobile_no
        self.weight = weight
