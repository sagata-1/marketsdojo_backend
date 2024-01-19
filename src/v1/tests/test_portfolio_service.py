# test_portfolio.py
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import Flask

app = Flask(__name__)
encoded_password = quote_plus("Saucepan03@!")

app.config['SQLALCHEMY_DATABASE_URI']= f"postgresql://postgres:{encoded_password}@db.krvuffjhmqiyerbpgqtv.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TokenModel(db.Model):
    __tablename__ = 'tokens_userid'

    id = db.Column(db.Integer, primary_key=True)  # int4 in SQL is represented as Integer in SQLAlchemy
    tokens = db.Column(db.Text)  # Text type for storing token strings

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
    
class PortfolioModel(db.Model):
    __tablename__ = 'portfolios'

    user_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    asset_type = db.Column(db.String, nullable=False)
    invested_amount = db.Column(db.Float, nullable=False)

    
def get_total_invested_amt(portfolio_entries):
    """
        Calculate the total invested amount from a list of portfolio entries.
        
        :param portfolio_entries: A list of dictionaries, where each dictionary represents a portfolio entry 
                                  and has a key 'invested_amount' with a numeric value.
        :type portfolio_entries: list(dict), 'invested_amount' in portfolio_entries
        :type portfolio_entries[i]['invested_amount']: float
        :return: The sum of all 'invested_amount' values from the portfolio entries.
        :rtype: float
    """
    return sum(item["invested_amount"] for item in portfolio_entries)

def get_portfolio(user_id):
    """
    Provide all portfolio entries for a given user.

    :param user_id: The user's ID
    :type user_id: int, > 0
    :return: A list of dictionaries, each representing a portfolio entry
    :rtype: list(dict)
    """
    portfolio_entries = PortfolioModel.query.filter_by(user_id=user_id).order_by(PortfolioModel.symbol).all()
    serialized_portfolio = [
        {
            "user_id": entry.user_id,
            "symbol": entry.symbol,
            "name": entry.name,
            "quantity": entry.quantity,
            "asset_type": entry.asset_type,
            "invested_amount": entry.invested_amount
        }
        for entry in portfolio_entries
    ]
    
    return serialized_portfolio

def get_user_from_token(access_token):
    """
        Retrieve a User object based on the provided access token.

        :param access_token: A string representing the access token.
        :return: User instance if a user is found with the given token, otherwise None.
        :rtype: dict
    """
    return User.query.filter_by(id=TokenModel.query.filter_by(tokens=access_token).first().id).first()
    
def portfolio_service(auth_header):
    """
    Show portfolio of stocks.

    :param access_token: The access token of the user
    :type access_token: str, != 0
    :return: A Flask response object with portfolio data and HTTP status code
    :rtype: tuple(dict, int)
    """
    code = 200
    if auth_header is None:
        code = 403
        response = {"error": {"code": 403, "message": "Missing access token"}}
    else:
        # Split the header to extract the token part
        parts = auth_header.split()
        if len(parts) == 2 and parts[0] == "Bearer":
            access_token = parts[1]
            id = TokenModel.query.filter_by(tokens=access_token).first()
            if not id:
                code = 403
                response = {"error": {"code": 403, "message": "Invalid access token"}}
        else:
            code = 403
            response = {"error": {"code": 403, "message": "Invalid Authorization header format"}}
            
    if code != 403:
        user = get_user_from_token(access_token)
        user_id = user.id
        cash = user.cash
        username = user.username
        portfolio_entries = get_portfolio(user_id)
        
        total_invested_amount = get_total_invested_amt(portfolio_entries)

        types = ["Stock (Equity)", "Forex", "Index", "ETF", "Commodity"] # CFD Support for later
        
        portfolio_data = {
            "portfolio": portfolio_entries,
            "cash": cash,
            "total_invested_amount": total_invested_amount,
            "starting_amt": 10000,
            "username": username,
            "types": types
        }
        response = portfolio_data

    return (response, code)