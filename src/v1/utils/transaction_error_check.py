from utils.lookup import lookup
from utils.get_asset import get_asset

def transaction_error_check(data, user, time, asset):
    """
        Perform error checks for a transaction.

        :param data: A dictionary containing transaction details with the keys 'symbol', 'quantity', 'asset_type', and 'action'.
        :type data: dict
        :param user: User object involved in the transaction.
        :type user: dict
        :param time: The datetime object representing the current time.
        :type time: datetime, non-empty
        :param asset: A dictionary containing asset details from looking it up via api call or None.
        :type asset: dict

        :return: A dictionary with response code, message, and data.
        :rtype: dict
    """
    symbol = data.get("symbol")
    num_shares = data.get("quantity")
    asset_type = data.get("asset_type")
    action = data.get("action")
    response = {"code": 200, "message": "Success", "data": {}}
    if symbol == None or num_shares == None or asset_type == None or action == None:
        response =  {"code": 400, "message": "Missing or incorrect query parameters", "data": {}}
    else:
        symbol = symbol.upper()
        action = action.lower()
        if action not in ["buy", "sell"]:
            response = {"code": 400, "message": "Invalid action", "data": {}}
    if response["code"] == 200:
        # Find open and close time
        open_time = time.replace(hour=8, minute=30)
        close_time = time.replace(hour=17, minute=0)
        # Can only buy when market is open
        if asset_type != "Forex":
            if open_time.date().weekday() == 5 or open_time.date().weekday() == 6:
                response =  {"code": 400, "message": "Cannot trade on a weekend!", "data": {}}
            if time < open_time or time > close_time:
                response = {"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}
        elif open_time.date().weekday() == 5 or (open_time.date().weekday() == 6 and time.hour < 18) or (open_time.date().weekday == 4 and time.hour > 16):
            response =  {"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}
                    
    if response["code"] == 200:
        if action == "buy":
            # Basic error checking (i.e. missing symbol, too many shares bought etc)
            if not asset:
                response =  {"code": 400, "message": "Invalid Symbol", "data": {}}
            elif (type(num_shares) != int) or num_shares <= 0:
                response =  {"code": 400, "message": "quantity must be a positive integer!", "data": {}}
            else:
                price = asset["price"]
                if (num_shares * price) > user.cash: 
                    response = {"code": 400, "message": "Cannot afford", "data":{}}
            
        else:
            user_id = user.id
            # Query to find the portfolio entry
            valid_asset = get_asset(symbol, user_id, asset_type)
            # Check if valid_asset exists
            if not valid_asset:
                response = {"code": 400, "message": "Invalid symbol", "data" : {}}
            elif (type(num_shares) != int) or num_shares < 0:
                response =  {"code": 400, "message": "quantity must be a positive integer!", "data": {}}
            # Check if the operation results in negative share count
            elif valid_asset.quantity - num_shares < 0:
                response = {"code": 400, "message": "Too many shares", "data": {}}
    return response