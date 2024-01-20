from functools import wraps
from models.token_model import TokenModel
from flask import make_response, jsonify, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.headers
        auth_header = data.get("Authorization")
        code = 200
        if auth_header is None:
            code = 403
            response = make_response(jsonify({"error": {"code": 403, "message": "Missing access token"}}), 403)
        else:
            # Split the header to extract the token part
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                access_token = parts[1]
                id = TokenModel.query.filter_by(tokens=access_token).first()
                if not id:
                    code = 403
                    response = make_response(jsonify({"error": {"code": 403, "message": "Invalid access token"}}), 403)
            else:
                code = 403
                response = make_response(jsonify({"error": {"code": 403, "message": "Invalid Authorization header format"}}), 403)

        if code != 403:
            response = f(*args, **kwargs, access_token=access_token)
        return response

    return decorated_function