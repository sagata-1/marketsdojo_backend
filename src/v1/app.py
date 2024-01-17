from flask import Flask, jsonify, make_response , request, Blueprint, register_blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .routes import blueprints

app=Flask(__name__)
CORS(app)
#register blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

#arman to fix up using his sessions knowledge. but db created here and imported in __init__.py of the subfolder whose function needs to access it
db=SQLAlchemy()

#use different URIs for different environments so we can add/remove columns/tables without breaking production code
#see pramods structure of having a config folder with test, dev and prod db
app.config['SQLALCHEMY_DATABASE_URI']=''

db.init_app(app)