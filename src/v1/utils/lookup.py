import datetime
import requests
import uuid
def lookup(symbol, type):
    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Financial Modeling Prep API
    if (type == "CFD"):
        url = f"https://marketdata.tradermade.com/api/v1/live?api_key=XZas9_pK9fByyYTKXbUa&currency={symbol}"
    else:
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=6fbceaefb411ee907e9062098ef0fd66"

    metal_dict = {
        "XAUUSD": "Gold",
        "XAGUSD": "Silver",
        "XPTUSD": "Platinum",
        "XPDUSD": "Palladium"
    }

    # Query API
    try:
        result = True
        if type not in ["CFD", "Forex", "Commodity", "Index", "ETF", "Stock (Equity)"]:
            result = None
        if result:
            response = requests.get(url,
            cookies={"session": str(uuid.uuid4())},
            headers={"User-Agent": "python-requests", "Accept": "*/*"},
            )
            quotes = response.json()
            if type == "CFD":
                quotes = quotes["quotes"][0]
                price = round(float(quotes["mid"]), 2)
                if quotes.get("instrument"):
                    result =  {"name": quotes["instrument"], "price": price, "symbol": quotes["instrument"], "exchange": "CFD"}
                else:
                    result = {"name": metal_dict[symbol], "price": price, "symbol": symbol, "exchange": "CFD"}
            else:
                price = round(float(quotes[0]["price"]), 2)
                result =  {"name": quotes[0]["name"], "price": price, "symbol": quotes[0]["symbol"], "exchange": quotes[0]["exchange"]}
    except (requests.RequestException, ValueError, KeyError, IndexError):
        result = None
    return result