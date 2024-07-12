from ..website import db

class CSV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    