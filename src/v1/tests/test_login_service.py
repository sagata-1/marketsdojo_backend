# test_login.py
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import Flask

app = Flask(__name__)
encoded_password = quote_plus("Saucepan03@!")

app.config['SQLALCHEMY_DATABASE_URI']= f"postgresql://postgres:{encoded_password}@db.krvuffjhmqiyerbpgqtv.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TokenModel(db.Model):
    __tablename__ = 'tokens_userid'

    id = db.Column(db.Integer, primary_key=True)  # int4 in SQL is represented as Integer in SQLAlchemy
    tokens = db.Column(db.Text)  # Text type for storing token strings

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    cash = db.Column(db.Float, nullable=False, default=10000.0) 
    bought = db.Column(db.BigInteger, nullable=False, default=0)
    sold = db.Column(db.BigInteger, nullable=False, default=0)
    timestamp = db.Column(db.DateTime(timezone=True)) 
    

    
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

    # Query user by email
    user = User.query.filter_by(email=email).first()

    # Check user exists and password is correct
    if not user or not check_password_hash(user.hash, password):
        response = {"error": {"code": 403, "message": "Incorrect email and/or password"}}

    # Query access token
    else:
        access_token = TokenModel.query.filter_by(id=user.id).first()
        response = {
            "username": user.username,
            "user_id": user.id,
            "email": email,
            "access_token": access_token.tokens
        }
    return response

def login_api(data):
    """
    Flask route for user login.

    Inputs:
    None (uses Flask request context)

    Outputs:
    Flask Response: JSON response containing user info and token, or an error message.
    """
    
    email = data.get("email")
    password = data.get("password")
    if not email:
        code = 403
        response = {"error": {"code": 403, "message": "email not provided"}}

    elif not password:
        code = 403
        response = {"error": {"code": 403, "message": "Did not enter a password"}}
    
    else:
        result = login_user(email, password)
        if "error" in result:
            code = 403
            response = result
        else:
            code = 200
            response = result

    return (response, code)