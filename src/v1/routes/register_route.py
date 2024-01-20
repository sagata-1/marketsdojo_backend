from . import register_route_1
from flask import jsonify, request, make_response
from services.register_service import register_user

@register_route_1.route("/v1/users", methods=['POST'])
def register():
    """
    API endpoint for user registration.

    Inputs:
    - None (uses Flask request context)

    Outputs:
    - A Flask JSON response with user details or error message, and HTTP status code.

    Preconditions:
    - Expects 'username', 'email', and 'password' in JSON request body.

    Postconditions:
    - Returns a JSON response with either registered user information or an error message.
    - Includes appropriate HTTP status code.
    """

    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        response = make_response(jsonify({"error": "Missing required fields"}), 400)
    else:
        response = register_user(username, email, password)
    return response