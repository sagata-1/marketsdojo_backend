from utils.database import db

class PortfolioModel(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    asset_type = db.Column(db.String, nullable=False)
    invested_amount = db.Column(db.Float, nullable=False)
