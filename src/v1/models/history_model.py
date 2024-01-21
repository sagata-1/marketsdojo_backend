from utils.database import db

class HistoryModel(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    symbol = db.Column(db.String, nullable=False)
    time_of_transaction = db.column(db.Datetime, nullable=False)
    transaction_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    invested_amount_per_transaction = db.Column(db.Float, nullable=False)
