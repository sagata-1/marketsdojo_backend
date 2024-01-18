from flask import Flask, jsonify, make_response , request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes import blueprints
from urllib.parse import quote_plus
from utils.database import db
from utils.create_token import create_token
from utils.jwt import jwt

app=Flask(__name__)
CORS(app)
encoded_password = quote_plus("Saucepan03@!")
#register blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint, url_prefix='/')
    print(blueprint)
#arman to fix up using his sessions knowledge. but db created here and imported in __init__.py of the subfolder whose function needs to access it


#use different URIs for different environments so we can add/remove columns/tables without breaking production code
#see pramods structure of having a config folder with test, dev and prod db
app.config['SQLALCHEMY_DATABASE_URI']= f"postgresql://postgres:{encoded_password}@db.krvuffjhmqiyerbpgqtv.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Import models after creating 'db'
from models.user_model import User
# Configure app JWT secret key for token generation
app.config['JWT_SECRET_KEY'] = 'RANDOM_KEY_THAT_IS_SECRET'
jwt.init_app(app)


with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")