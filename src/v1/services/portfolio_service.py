# portfolio_service.py
from utils.get_user_from_token import get_user_from_token
from utils.get_portfolio import get_portfolio
from utils.get_total_invested_amt import get_total_invested_amt
from flask import jsonify, make_response

def portfolio_service(access_token):
    """
    Show portfolio of stocks.

    :param access_token: The access token of the user
    :type access_token: str, != 0
    :return: A Flask response object with portfolio data and HTTP status code
    :rtype: tuple(dict, int)
    """
    response = {}
    code = 200

    user = get_user_from_token(access_token)
    user_id = user.id
    cash = user.cash
    username = user.username
    portfolio_entries = get_portfolio(user_id)
    
    total_invested_amount = get_total_invested_amt(portfolio_entries)
    
    portfolio_data = {"code": 200, "message": "Success", "data": {
        "portfolio": portfolio_entries,
        "available_cash": cash,
        "total_invested_amount": total_invested_amount,
        "starting_amt": 10000.0,
        "username": username
    }}
    response = jsonify(portfolio_data)

    return make_response(response, code)
