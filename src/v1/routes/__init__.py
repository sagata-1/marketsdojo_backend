from v1.services.buy_service import buy_service
from v1.services.register_service import register_service
#add more services here

buy_route = Blueprint("buy_route", __name__)
register_route = Blueprint('register', __name__)
login_route=Blueprint('login',__name__)
#add more routes here and add them to the blueprints list below


blueprints=[buy_route,register_route,login_route]

