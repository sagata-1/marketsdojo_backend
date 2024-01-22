from . import history_route_1
from flask import request, make_response, jsonify
from services.record_transaction_service import record_transaction_service
from utils.login_required import login_required

@history_route_1.route("/v1/users/history", methods=["GET", "POST"])
@login_required
def history_api(access_token):
    """
    Handles requests to the history API endpoint.

    :type access_token: str
    :param access_token: The access token used for authentication.

    :rtype: Response
    :return: A Flask response object containing the API response and status code.
    """
    if request.method == "POST":
        response = record_transaction_service(request.json, access_token)
    else:
        response = make_response(jsonify({"code": 302, "message": "History route get method to be implemented", "data": {}}), 302)
    return response