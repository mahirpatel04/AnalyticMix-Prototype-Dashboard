from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class CSV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    files = db.relationship('CSV')