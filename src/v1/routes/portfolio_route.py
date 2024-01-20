from . import portfolio_route_1
from flask import jsonify, request, make_response
from services.portfolio_service import portfolio_service
from utils.login_required import login_required


@portfolio_route_1.route("/v1/users/portfolio", methods=['GET'])
@login_required
def portfolio(access_token):
    """
    Show portfolio of stocks.

    :param access_token: The access token of the user
    :type access_token: str, != 0
    :return: A Flask response object with portfolio data and HTTP status code
    :rtype: tuple(dict, int)
    """
    return portfolio_service(access_token)