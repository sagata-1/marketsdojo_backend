from utils.database import db
from utils.lookup import lookup
from models.history_model import HistoryModel

"""
	Update the history table after a user buys or sells an asset.

	:param data: A dictionary containing transaction details with keys like 'symbol', 'quantity', 'action'.
	:type data: dict
	:param user: User object involved in the transaction.
	:type user: dict
	:param time: The datetime object representing the time of transaction.
	:type time: datetime
	:param asset: A dictionary containing asset details.
	:type asset: dict

	:return: A dictionary with response code, message, and data.
	:rtype: dict
	
	Precondition:
        - user_id is the id of the user who is buying or selling.
        - symbol is the symbol of the asset the user is transacting.
        - transaction_price is the current market price.
        - quantity is the number of units of the asset.
        - transaction_time is the timestamp when transaction occurred and is valid.

	Postcondition:
		- The invested_amount_per_transaction in history is equal to price multiplied by quantity.
		- The history table includes the current transaction record.
		- Returns true (via 'code': 200) if history table is successfully updated, false otherwise.
"""

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