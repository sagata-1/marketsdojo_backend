from . import login_route_1
from flask import jsonify, request, make_response
from services.login_service import login_user


@login_route_1.route("/v1/users/login", methods=['POST'])
def login():
    """
    Flask route for user login.

    Inputs:
    None (uses Flask request context)

    Outputs:
    Flask Response: JSON response containing user info and token, or an error message.
    """
    
    data = request.json
    email = data.get("email")
    password = data.get("password")
    response = login_user(email, password)

    return make_response(jsonify(response), response["code"])