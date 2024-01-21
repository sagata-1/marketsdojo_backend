from utils.transaction_error_check import transaction_error_check
from utils.get_user_from_token import get_user_from_token
from utils.update_users_table_after_transaction import update_users_table_after_transaction
from utils.update_history_table_after_transaction import update_history_table_after_transaction
from flask import make_response, jsonify

def record_transaction_service(data, access_token):
    user = get_user_from_token(access_token)
    response = transaction_error_check(data, user)
    if response["code"] == 200:
        response = update_history_table_after_transaction(data, user)
        if response["code"] == 200:
            response = update_portfolios_table_after_transaction(data, user)
            if response["code"] == 200:
                response = update_users_table_after_transaction(data, user)
            
    return make_response(jsonify(response), response["code"])