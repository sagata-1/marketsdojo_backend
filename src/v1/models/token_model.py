# token_model.py
from utils.database import db
 
class TokenModel(db.Model):
    __tablename__ = 'tokens_userid'

    id = db.Column(db.Integer, primary_key=True)  # int4 in SQL is represented as Integer in SQLAlchemy
    tokens = db.Column(db.Text)  # Text type for storing token strings
