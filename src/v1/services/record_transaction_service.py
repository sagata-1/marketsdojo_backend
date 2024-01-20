from utils.transaction_error_check import transaction_error_check
from utils.get_user_from_token import get_user_from_token
from flask import make_response, jsonify

def record_transaction_service(data, access_token):
    response = transaction_error_check(data)
    if response["code"] == 200:
        user = get_user_from_token(access_token)
        response = update_history_table_after_transaction(data, user)
        if response["code"] == 200:
            response = update_portfolios_table_after_transaction(data, user)
            
    return make_response(jsonify(response), response["code"])