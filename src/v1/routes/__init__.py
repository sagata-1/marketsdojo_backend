from flask import Blueprint
#add more services here

history_route_1 = Blueprint("history", __name__)
register_route_1 = Blueprint('register', __name__)
login_route_1 = Blueprint('login',__name__)
portfolio_route_1 = Blueprint('portfolio', __name__)
#add more routes here and add them to the blueprints list below

# execute the routes
from . import history_route, login_route, register_route, portfolio_route

blueprints=[history_route_1,register_route_1,login_route_1, portfolio_route_1]

