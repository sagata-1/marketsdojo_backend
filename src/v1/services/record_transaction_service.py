from utils.transaction_error_check import transaction_error_check
from utils.get_user_from_token import get_user_from_token
from utils.update_users_table_after_transaction import update_users_table_after_transaction
from utils.update_history_table_after_transaction import update_history_table_after_transaction
from utils.update_portfolios_table_after_transaction import update_portfolios_table_after_transaction
from utils.compute_transaction_time import compute_transaction_time
from utils.lookup import lookup
from flask import make_response, jsonify

def record_transaction_service(data, access_token):
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
    time = compute_transaction_time()
    response = transaction_error_check(data, user, time, asset)
    if response["code"] == 200:
        response = update_history_table_after_transaction(data, user, time, asset)
        if response["code"] == 200:
            response = update_portfolios_table_after_transaction(data, user, asset)
            if response["code"] == 200:
                response = update_users_table_after_transaction(data, user, asset)
            
    return make_response(jsonify(response), response["code"])