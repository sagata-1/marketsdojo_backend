from functools import wraps
from models.token_model import TokenModel
from flask import make_response, jsonify

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.headers
        access_token = data.get("Authorization")
        code = 200
        if access_token is None:
            code = 403
            response = make_response(jsonify({"error": {"code": 403, "message": "Missing access token"}}), 403)
        else:
            id = TokenModel.query.filter_by(tokens=access_token).first().id
            if len(id) != 1:
                code = 403
                response = make_response(jsonify({"error": {"code": 403, "message": "Missing access token"}}), 403)
        if code != 403:
            response = f(*args, **kwargs, access_token=access_token)
        return response

    return decorated_function