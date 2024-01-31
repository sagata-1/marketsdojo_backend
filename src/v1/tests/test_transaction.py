# test_transaction.py
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import Flask
import datetime
import requests
import uuid
import pytz

app = Flask(__name__)
encoded_password = quote_plus("Saucepan03@!")

app.config['SQLALCHEMY_DATABASE_URI']= f"postgresql://postgres.krvuffjhmqiyerbpgqtv:{encoded_password}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class HistoryModel(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    symbol = db.Column(db.String, nullable=False)
    time_of_transaction = db.Column(db.DateTime, nullable=False)
    transaction_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    invested_amount_per_transaction = db.Column(db.Float, nullable=False)
    
class PortfolioModel(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    asset_type = db.Column(db.String, nullable=False)
    invested_amount = db.Column(db.Float, nullable=False)

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

class TokenModel(db.Model):
    __tablename__ = 'tokens_userid'

    id = db.Column(db.Integer, primary_key=True)  # int4 in SQL is represented as Integer in SQLAlchemy
    tokens = db.Column(db.Text)  # Text type for storing token strings
    
def get_user_from_token(access_token):
    """
        Retrieve a User object based on the provided access token.

        :param access_token: A string representing the access token.
        :return: User instance if a user is found with the given token, otherwise None.
        :rtype: dict
    """
    return User.query.filter_by(id=TokenModel.query.filter_by(tokens=access_token).first().id).first()

def get_asset(symbol, user_id, asset_type):
    """
    Retrieves the first asset matching the given criteria from the PortfolioModel.

    :type symbol: str
    :param symbol: The symbol of the asset.

    :type user_id: int
    :param user_id: The user's ID.

    :type asset_type: str
    :param asset_type: The type of the asset.

    :rtype: PortfolioModel or None
    :return: The first asset found that matches the criteria or None if no match is found.
    """
    return PortfolioModel.query.filter_by(symbol=symbol, user_id=user_id, asset_type=asset_type).first()

def lookup(symbol, type):
    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Financial Modeling Prep API
    if (type == "CFD"):
        url = f"https://marketdata.tradermade.com/api/v1/live?api_key=XZas9_pK9fByyYTKXbUa&currency={symbol}"
    else:
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=6fbceaefb411ee907e9062098ef0fd66"

    metal_dict = {
        "XAUUSD": "Gold",
        "XAGUSD": "Silver",
        "XPTUSD": "Platinum",
        "XPDUSD": "Palladium"
    }

    # Query API
    try:
        result = True
        if type not in ["CFD", "Forex", "Commodity", "Index", "ETF", "Stock (Equity)"]:
            result = None
        if result:
            response = requests.get(url,
            cookies={"session": str(uuid.uuid4())},
            headers={"User-Agent": "python-requests", "Accept": "*/*"},
            )
            quotes = response.json()
            if type == "CFD":
                quotes = quotes["quotes"][0]
                price = round(float(quotes["mid"]), 2)
                if quotes.get("instrument"):
                    result =  {"name": quotes["instrument"], "price": price, "symbol": quotes["instrument"], "exchange": "CFD"}
                else:
                    result = {"name": metal_dict[symbol], "price": price, "symbol": symbol, "exchange": "CFD"}
            else:
                price = round(float(quotes[0]["price"]), 2)
                result =  {"name": quotes[0]["name"], "price": price, "symbol": quotes[0]["symbol"], "exchange": quotes[0]["exchange"]}
    except (requests.RequestException, ValueError, KeyError, IndexError):
        result = None
    return result

def transaction_error_check(data, user, time, asset):
    """
        Perform error checks for a transaction.

        :param data: A dictionary containing transaction details with the keys 'symbol', 'quantity', 'asset_type', and 'action'.
        :type data: dict
        :param user: User object involved in the transaction.
        :type user: dict
        :param time: The datetime object representing the current time.
        :type time: datetime, non-empty
        :param asset: A dictionary containing asset details from looking it up via api call or None.
        :type asset: dict

        :return: A dictionary with response code, message, and data.
        :rtype: dict
    """
    symbol = data.get("symbol")
    num_shares = data.get("quantity")
    asset_type = data.get("asset_type")
    action = data.get("action")
    response = {"code": 200, "message": "Success", "data": {}}
    if symbol == None or num_shares == None or asset_type == None or action == None:
        response =  {"code": 400, "message": "Missing or incorrect query parameters", "data": {}}
    else:
        symbol = symbol.upper()
        action = action.lower()
        if action not in ["buy", "sell"]:
            response = {"code": 400, "message": "Invalid action", "data": {}}
    if response["code"] == 200:
        # Find open and close time
        open_time = time.replace(hour=8, minute=30)
        close_time = time.replace(hour=17, minute=0)
        # Can only buy when market is open
        if asset_type != "Forex":
            if open_time.date().weekday() == 5 or open_time.date().weekday() == 6:
                response =  {"code": 400, "message": "Cannot trade on a weekend!", "data": {}}
            if time < open_time or time > close_time:
                response = {"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}
        elif open_time.date().weekday() == 5 or (open_time.date().weekday() == 6 and time.hour < 18) or (open_time.date().weekday == 4 and time.hour > 16):
            response =  {"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}
                    
    if response["code"] == 200:
        if action == "buy":
            # Basic error checking (i.e. missing symbol, too many shares bought etc)
            if not asset:
                response =  {"code": 400, "message": "Invalid Symbol", "data": {}}
            elif (type(num_shares) != int) or num_shares <= 0:
                response =  {"code": 400, "message": "quantity must be a positive integer!", "data": {}}
            else:
                price = asset["price"]
                if (num_shares * price) > user.cash: 
                    response = {"code": 400, "message": "Cannot afford", "data":{}}
            
        else:
            user_id = user.id
            # Query to find the portfolio entry
            valid_asset = get_asset(symbol, user_id, asset_type)
            # Check if valid_asset exists
            if not valid_asset:
                response = {"code": 400, "message": "Invalid symbol", "data" : {}}
            elif (type(num_shares) != int) or num_shares < 0:
                response =  {"code": 400, "message": "quantity must be a positive integer!", "data": {}}
            # Check if the operation results in negative share count
            elif valid_asset.quantity - num_shares < 0:
                response = {"code": 400, "message": "Too many shares", "data": {}}
    return response

def update_history_table_after_transaction(data, user, time, asset):
	user_id = user.id
	symbol = data.get("symbol").upper()
	num_shares = data.get("quantity")
	action = data.get("action").lower()
	price = asset["price"]
	response = {"code": 200, "message": "Success", "data": {}}
	if action == "buy":
		try:
			new_history = HistoryModel(
			user_id=user_id,
			symbol=symbol,
			transaction_price=price,
			quantity=num_shares,
			invested_amount_per_transaction=num_shares * price,
			time_of_transaction=time
			)

			# Add the new record to the session and commit it
			db.session.add(new_history)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			response =  {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
	else:
		num_shares *= -1
		try:
			new_history = HistoryModel(
			user_id=user_id,
			symbol=symbol,
			transaction_price=price,
			quantity=num_shares,
			invested_amount_per_transaction=num_shares * price,
			time_of_transaction=time
			)

			# Add the new record to the session and commit it
			db.session.add(new_history)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			response =  {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
	
	return response

def calculate_portfolio_invested_amount(symbol, user_id):
    """
    Calculates the total invested amount for a specific symbol and user.

    :param symbol: The asset symbol to query in the history table.
    :type symbol: str
    :param user_id: The ID of the user.
    :type user_id: int
    :return: Total invested amount for the given symbol and user.
    :rtype: float
    """
    return db.session.query(db.func.sum(HistoryModel.invested_amount_per_transaction)).filter_by(symbol=symbol, user_id=user_id).scalar()

def update_portfolios_table_after_transaction(data, user, asset):
    """
    Updates the portfolios table after a transaction (buy or sell) is made.

    :type data: dict
    :param data: The transaction data containing symbol, quantity, action, and asset_type.

    :type user: User
    :param user: The user performing the transaction.

    :type asset: dict
    :param asset: The asset involved in the transaction.

    :rtype: dict
    :return: A response dictionary with status code, message, and data.
    """
    symbol = data.get("symbol").upper()
    num_shares = data.get("quantity")
    action = data.get("action").lower()
    asset_type = data.get("asset_type")
    user_id = user.id
    response = {"code": 200, "message": "Success", "data": {}}
    asset_exists = get_asset(symbol, user_id, asset_type)
    if action == "buy":
        if not asset_exists:
            try:
                new_portfolio_entry = PortfolioModel(
                user_id=user_id,
                name=asset["name"],
                symbol=symbol,
                invested_amount=calculate_portfolio_invested_amount(symbol, user_id),
                quantity=num_shares,
                asset_type=asset_type
                )
                db.session.add(new_portfolio_entry)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
        else:
            try:
                asset_exists.quantity += num_shares
                asset_exists.invested_amount = calculate_portfolio_invested_amount(symbol, user_id)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
    else:
        if asset_exists.quantity - num_shares == 0:
            try:
                db.session.delete(asset_exists)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": {}}
        else:
            try:
                asset_exists.quantity -= num_shares
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = {"code": 400, "message": "Transaction failed, rollback performed", "data": {}}
    return response

def update_users_table_after_transaction(data, user, asset):
    """
    Update user's cash, bought, and sold values in the users table after a transaction.

    :type data: dict
    :type user: User
    :type asset: dict
    :rtype: dict

    :param data: A dictionary containing transaction details with keys like 'quantity', 'action'.
    :param user: User object involved in the transaction.
    :param asset: A dictionary containing asset details with key 'price'.

    :return: A dictionary with response code, message, and data.

    Preconditions:
    - 'quantity' in data should be an integer.
    - 'action' in data should be a string ('buy' or 'sell').
    - 'price' in asset should be a float or integer.

    Postconditions:
    - User's cash is updated according to the transaction (decreased for buy, increased for sell).
    - User's 'bought' or 'sold' count is incremented based on the action.
    - Returns a response dictionary with a success or error message.
    """
    num_shares = data.get("quantity")
    action = data.get("action").lower()
    price = asset["price"]
    response = {"code": 200, "message": "Success", "data": {}}
    if action == "buy":
        try:
            user.cash -= num_shares * price
            user.bought += 1
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
    else:
        try:
            user.cash += num_shares * price
            user.sold += 1
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response = {"code": 400, "message": "Transaction failed, rollback performed", "data": str(e)}
    return response

def record_transaction_service(data, access_token, time):
    """
    Records a transaction and updates various tables based on the transaction data.

    :type data: dict
    :param data: The transaction data containing necessary details like symbol, quantity, etc.

    :type access_token: str
    :param access_token: The access token to identify and authenticate the user.

    :rtype: Response
    :return: A Flask response object with the transaction response and status code.
    """
    user = get_user_from_token(access_token)
    asset = lookup(data.get("symbol").upper(), data.get("asset_type"))
    response = transaction_error_check(data, user, time, asset)
    if response["code"] == 200:
        response = update_history_table_after_transaction(data, user, time, asset)
        if response["code"] == 200:
            response = update_portfolios_table_after_transaction(data, user, asset)
            if response["code"] == 200:
                response = update_users_table_after_transaction(data, user, asset)
            
    return (response, response["code"])