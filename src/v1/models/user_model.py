# user_model.py
from utils.database import db 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    cash = db.Column(db.Float, nullable=False, default=10000.0) 
    bought = db.Column(db.BigInteger, nullable=False, default=0)
    sold = db.Column(db.BigInteger, nullable=False, default=0)
    timestamp = db.Column(db.DateTime(timezone=True)) 
    

    