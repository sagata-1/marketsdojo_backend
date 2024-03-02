from functools import wraps
from models.token_model import TokenModel
from models.user_model import UserModel
from flask import make_response, jsonify, request

'''
    This function checks if the user is an admin.
    If the user is not an admin it returns a 403 error.
    If the user is an admin it returns the response of the function it decorates and access token.
'''

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.headers
        auth_header = data.get("Authorization")
        code = 200
        if auth_header is None:
            code = 403
            response = make_response(jsonify({"code": 403, "message": "Missing access token", "data": {}}), 403)
        else:
            # Split the header to extract the token part
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                access_token = parts[1]
                user_id = TokenModel.query.filter_by(tokens=access_token).first().id
                print(user_id)
                role= UserModel.query.filter_by(id=user_id).first().role
                if role != "admin_user":
                    code = 403
                    response = make_response(jsonify({"code": 403, "message": "Unauthorized access", "data": {}}), 403)
                if not user_id:
                    code = 403
                    response = make_response(jsonify( {"code": 403, "message": "Invalid access token", "data": {}}), 403)
            else:
                code = 403
                response = make_response(jsonify({"code": 403, "message": "Invalid Authorization header format", "data": {}}), 403)

        if code != 403:
            response = f(*args, **kwargs)
        return response

    return decorated_function