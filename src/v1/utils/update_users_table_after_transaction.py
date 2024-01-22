# update_users_table_after_transaction.py
from utils.database import db

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