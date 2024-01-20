from . import history_route_1
from flask import request
from services.record_transaction_service import record_transaction_service
from utils.login_required import login_required

@history_route_1.route("/v1/users/history", methods=["GET", "POST"])
@login_required
def buy_api(access_token):
    if request.method == "POST":
        return record_transaction_service(request.json, access_token)
    else:
        return "History route to be implemented"