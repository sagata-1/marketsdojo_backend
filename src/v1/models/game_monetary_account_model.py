# user_model.py
from utils.database import db

class GameMonetaryAccountModel(db.Model):
    __tablename__ = 'game_monetary_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    game_id= db.Column(db.Integer, nullable=False)
    available_balance = db.Column(db.Float, nullable=False)
    gross_invested_amount= db.Column(db.Float, nullable=False)
    total_buy_transactions = db.Column(db.BigInteger, nullable=False, default=0)
    total_sell_transactions = db.Column(db.BigInteger, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True),default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True))


