from extension import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(250),unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(250))
    admin = db.Column(db.Boolean)

    def __init__(self,name,password,public_id,admin):
        self.name = name
        self.password = password
        self.admin = admin
        self.public_id = public_id
