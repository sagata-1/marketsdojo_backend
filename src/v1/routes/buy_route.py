from . import buy_route_1

'''
Q: What are the inputs to this function?
A: Who is buying, what is he buying, how much is buying, at what price is he buying, when did he buy this?
    1. Asset Type
    2. Symbol
    3. Quantity
    4. Current Market price (price at the time he clicked buy)
    5. Time of Transaction
    6. user_id (access_token, who is buying)
'''

@buy_route_1.route("/v1/users/history", methods=["POST"])
# @login_required
def buy_api(access_token):
    return buy_service(access_token,request.json)
