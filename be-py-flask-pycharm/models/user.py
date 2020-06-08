from db import db


class UserModel(db.Model):
    __table__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, index=True)
    password_has = db.Column(db.String(129))
