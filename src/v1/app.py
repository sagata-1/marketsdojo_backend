from flask import Flask, jsonify, make_response , request, Blueprint, register_blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

app=Flask(__name__)
CORS(app)

#use different URIs for different environments so we can add/remove columns/tables without breaking production code
app.config['SQLALCHEMY_DATABASE_URI']=''

db.init_app(app)