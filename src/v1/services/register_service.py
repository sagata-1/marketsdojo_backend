# services/register_service.py
from werkzeug.security import generate_password_hash
from models.user_model import User, db
from models.token_model import TokenModel
from utils.create_token import create_token  # Replace with the actual import
from sqlalchemy.exc import IntegrityError
from flask import make_response, jsonify

def register_user(username: str, email: str, password: str) -> (dict, int):
    """
    Register a new user.

    Inputs:
    - username (str): The username of the new user.
    - email (str): The email of the new user.
    - password (str): The password of the new user.

    Outputs:
    - A tuple containing:
      - A dictionary with user details or error message.
      - An integer HTTP status code.

    Preconditions:
    - username, email, and password are non-empty strings.

    Postconditions:
    - If registration is successful, returns user details and status code 200.
    - If user already exists, returns an error message and status code 400.
    - If database error occurs, returns an error message and status code 500.
    """

    code = 200
    if User.query.filter((User.username == username) | (User.email == email)).first():
        code = 400
        response = jsonify({"error": "Username or email already exists"})

    else:
        new_user = User(username=username, email=email, hash=generate_password_hash(password))
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            code = 500
            response = jsonify({"error": "Database error occurred"})

        access_token = create_token(new_user.id, new_user.username)

        new_token = TokenModel(id=new_user.id, tokens=access_token)
        db.session.add(new_token)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            code = 500
            response = jsonify({"error": "Database error occurred"})
            
    if code == 200:
        response = {"username": username, "user_id": new_user.id, "email": email, "access_token": access_token}
            

    return make_response(response, code)
