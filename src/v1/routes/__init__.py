from services import buy_service
from services import register_service
from flask import Blueprint
#add more services here

buy_route_1 = Blueprint("buy", __name__)
register_route_1 = Blueprint('register', __name__)
login_route_1 = Blueprint('login',__name__)
portfolio_route_1 = Blueprint('portfolio', __name__)
#add more routes here and add them to the blueprints list below

# execute the routes
from . import buy_route, login_route, register_route, portfolio_route

blueprints=[buy_route_1,register_route_1,login_route_1, portfolio_route_1]

