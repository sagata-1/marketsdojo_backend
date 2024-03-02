from . import games_route_1 
from flask import jsonify, request, make_response
from utils.admin_login_required import admin_login_required
from services.games_service import increment_available_balance_by_game_id

'''
Handles requests to the increment available balance API endpoint.
Contract: ToDo
'''

@games_route_1.route("v1/games/<int:game_id>/actions/increment_available_balance", methods=['POST'])
@admin_login_required
def increment_available_balance_by_game_id_route(game_id):
    data = request.json
    balance_increment = data.get("balance_increment")
    response=increment_available_balance_by_game_id(game_id,balance_increment)
    return response


