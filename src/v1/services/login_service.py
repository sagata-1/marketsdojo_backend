# login_service.py
from werkzeug.security import check_password_hash
from models.user_model import User
from models.token_model import TokenModel

def login_user(email, password):
    """
    Authenticate a user.

    Inputs:
    email (str): The email of the user.
    password (str): The password of the user.

    Output:
    response: A dictionary containing user info and token if authentication is successful, 
          or an error message if not.
    """
    if not email:
        response = {"code": 403, "message": "email not provided", "data": {}}

    elif not password:
        response = {"code": 403, "message": "Did not enter a password", "data": {}}
    
    else:
        # Query user by email
        user = User.query.filter_by(email=email).first()

        # Check user exists and password is correct
        if not user or not check_password_hash(user.hash, password):
            response = {"code": 403, "message": "Incorrect email and/or password", "data": {}}

        # Query access token
        else:
            access_token = TokenModel.query.filter_by(id=user.id).first()
            response = {"code": 200, "message": "Success", "data": {
                "username": user.username,
                "user_id": user.id,
                "email": email,
                "access_token": access_token.tokens
            }}
    return response