from backend import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    files = db.relationship('CSV')
    
    user_type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }

class AdminUser(User):
    __tablename__ = None  # Avoid creating a separate table for Admin

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }