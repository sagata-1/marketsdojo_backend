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
    result = login_user(email, password)
    if "error" in result:
        code = 403
        response = jsonify(result) 
    else:
        code = 200
        response = jsonify(result) 

    return make_response(response, code)