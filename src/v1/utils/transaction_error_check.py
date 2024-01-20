from utils.lookup import lookup
import datetime
import pytz

def transaction_error_check(data):
    symbol = data.get("symbol")
    num_shares = data.get("quantity")
    asset_type = data.get("type")
    action = data.get("action")

    if action == "buy":
        response = {"code": 200, "message": "No errors yet"}
        if symbol == None or num_shares == None or asset_type == None:
            response =  {"code": 400, "message": "Missing or incorrect query parameters"}
        if response["code"] == 200:
            # Basic error checking (i.e. missing symbol, too many shares bought etc)
            symbol = symbol.upper()
            stock = lookup(symbol, asset_type)
            if not stock:
                response =  {"code": 400, "message": "Invalid Symbol"}
            elif (type(num_shares) != int):
                response =  {"code": 400, "message": "quantity must be an integer!"}
            elif num_shares < 1:
                response = {"code": 400, "message": "Invalid shares"}
            # Create a datetime object in UTC
            utc_dt = datetime.datetime.now(pytz.timezone("UTC"))
            price = stock["price"]

            # Convert the datetime object to UTC-5 timezone
            utc_minus_5_dt = utc_dt.astimezone(pytz.timezone('Etc/GMT+5'))
            open_time = utc_minus_5_dt.replace(hour=8, minute=30)
            close_time = utc_minus_5_dt.replace(hour=17, minute=0)
            time = utc_minus_5_dt
            # Can only buy when market is open
            if asset_type and asset_type != "Forex":
                if open_time.date().weekday() == 5 or open_time.date().weekday() == 6:
                    response =  {"code": 400, "message": "Cannot trade on a weekend!"}
                if time < open_time or time > close_time:
                    response = {"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)"}
            else:
                if open_time.date().weekday() == 5 or (open_time.date().weekday() == 6 and time.hour < 18) or (open_time.date().weekday == 4 and time.hour > 16):
                    response =  {"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)"}
            
        else:
            response = {"code": 302, "message": "To be implemented"}
        return response