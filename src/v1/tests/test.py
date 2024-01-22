import test_login_service
from test_login_service import login_api
import test_portfolio_service
from test_portfolio_service import portfolio_service
import test_transaction
from test_transaction import record_transaction_service
from test_transaction import get_asset
from datetime import datetime, timedelta, timezone
import pytz

def test_login():
    with test_login_service.app.app_context():
        assert(login_api({"email":"ajasuja1@jhu.edu", "password": "abcdefg"}) == ({"code": 200, "message": "Success", "data": {"username":"Arman Jasuja", "user_id": 26, "email": "ajasuja1@jhu.edu", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6IkFybWFuIEphc3VqYSIsImlhdCI6MTcwNDE5MDI5MiwianRpIjoiMWI4N2Q1OTQtNWVkMy00ZDk3LWEzNTAtMGJlMzhlOTU4NzA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjYsIm5iZiI6MTcwNDE5MDI5MiwiY3NyZiI6IjBlNTBjMTZjLTNjMWItNDY0Ny1hYWFlLTgwMDY3OTdiYWU2YSIsImV4cCI6MTcwNDE5MTE5Mn0.WC6XDZs3tVyEHT8y3WN0SVxEUVkAoBdKKCmfzF6OVlk"}}, 200))
        assert(login_api({"email":"ajasuja1@jhu.edu", "password": "abcdef"}) == ( {"code": 403, "message": "Incorrect email and/or password", "data": {}}, 403))
        assert(login_api({"emai":"ajasuja1@jhu.edu", "password": "abcdefg"}) == ({"code": 403, "message": "email not provided", "data": {}}, 403))
        assert(login_api({"email":"ajasuja1@jhu.edu", "passwor": "abcdefg"}) == ({"code": 403, "message": "Did not enter a password", "data": {}}, 403))
        
def test_portfolio():
    with test_portfolio_service.app.app_context():
        assert(portfolio_service("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6IkFybWFuIEphc3VqYSIsImlhdCI6MTcwNDE5MDI5MiwianRpIjoiMWI4N2Q1OTQtNWVkMy00ZDk3LWEzNTAtMGJlMzhlOTU4NzA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjYsIm5iZiI6MTcwNDE5MDI5MiwiY3NyZiI6IjBlNTBjMTZjLTNjMWItNDY0Ny1hYWFlLTgwMDY3OTdiYWU2YSIsImV4cCI6MTcwNDE5MTE5Mn0.WC6XDZs3tVyEHT8y3WN0SVxEUVkAoBdKKCmfzF6OVlk") == ({"code": 200, "message": "Success", "data": {
                "available_cash": 10000.0,
                "portfolio": [],
                "starting_amt": 10000.0,
                "total_invested_amount": 0,
                "username": "Arman Jasuja"
                }}, 200))
        
        assert(portfolio_service("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6IkFybWFuIEphc3VqYSIsImlhdCI6MTcwNDE5MDI5MiwianRpIjoiMWI4N2Q1OTQtNWVkMy00ZDk3LWEzNTAtMGJlMzhlOTU4NzA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjYsIm5iZiI6MTcwNDE5MDI5MiwiY3NyZiI6IjBlNTBjMTZjLTNjMWItNDY0Ny1hYWFlLTgwMDY3OTdiYWU2YSIsImV4cCI6MTcwNDE5MTE5Mn0.WC6XDZs3tVyEHT8y3WN0SVxEUVkAoBdKKCmfzF6OVl") == ({
                    "code": 403,
                    "message": "Invalid access token",
                    "data": {}
                }, 403))

        assert(portfolio_service("Beare eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6IkFybWFuIEphc3VqYSIsImlhdCI6MTcwNDE5MDI5MiwianRpIjoiMWI4N2Q1OTQtNWVkMy00ZDk3LWEzNTAtMGJlMzhlOTU4NzA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjYsIm5iZiI6MTcwNDE5MDI5MiwiY3NyZiI6IjBlNTBjMTZjLTNjMWItNDY0Ny1hYWFlLTgwMDY3OTdiYWU2YSIsImV4cCI6MTcwNDE5MTE5Mn0.WC6XDZs3tVyEHT8y3WN0SVxEUVkAoBdKKCmfzF6OVl") == ({
                    "code": 403,
                    "message": "Invalid Authorization header format",
                    "data": {}
                }, 403))

def test_transactions():
    utc_minus_5 = timezone(-timedelta(hours=5))
    valid_time = datetime(2023, 12, 18, 15, 30, tzinfo=utc_minus_5)
    post_trading_time = datetime(2023, 12, 18, 17, 30, tzinfo=utc_minus_5)
    pre_trading_time = datetime(2023, 12, 18, 7, 30, tzinfo=utc_minus_5)
    weekend_1 = datetime(2023, 12, 17, 10, 30, tzinfo=utc_minus_5)
    weekend_2 = datetime(2023, 12, 16, 10, 30, tzinfo=utc_minus_5)
    one_min_before_trading = datetime(2023, 12, 18, 8, 29, tzinfo=utc_minus_5)
    one_min_after_trading = datetime(2023, 12, 18, 17, 1, tzinfo=utc_minus_5)
    midnight_check = datetime(2023, 12, 18, 0, 0, tzinfo=utc_minus_5)
    with test_transaction.app.app_context():
        # Testing that purchases work on forex assets
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        asset  = get_asset("EURUSD", 2, "Forex")
        assert(asset.symbol == "EURUSD")
        assert(asset.asset_type == "Forex")
        assert(asset.quantity == 2)
        assert(record_transaction_service({"action": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        # Testing that purchases work on non-forex assets
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        # Testing that buying an already existing asset works
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        asset  = get_asset("AAPL", 2, "Stock (Equity)")
        assert(asset.symbol == "AAPL")
        assert(asset.asset_type == "Stock (Equity)")
        assert(asset.quantity == 4)
        # Testing that selling too many assets is not possible
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 5, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 400, "message": "Too many shares", "data": {}}, 400))
        asset  = get_asset("AAPL", 2, "Stock (Equity)")
        assert(asset.symbol == "AAPL")
        assert(asset.asset_type == "Stock (Equity)")
        assert(asset.quantity == 4)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        asset  = get_asset("AAPL", 2, "Stock (Equity)")
        assert(asset.symbol == "AAPL")
        assert(asset.asset_type == "Stock (Equity)")
        assert(asset.quantity == 2)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        # Testing that buying too many assets is not possible
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 20000000000000, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", valid_time) == ({"code": 400, "message": "Cannot afford", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_1) == ({"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}, 400))
        # Testing that Forex transactions do not work on weekends
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_2) == ({"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}, 400))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_1) == ({"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}, 400))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_2) == ({"code": 400, "message": "You cannot trade in the Forex market from 6:00 pm Friday to 4:00 pm on Sunday! (1 hour after the market closes and upto 1 hour before the market opens)", "data": {}}, 400))       
        assert(get_asset("EURUSD", 2, "Forex") == None)
        # Testing that non-Forex transactions do not work on weekends
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_1) == ({"code": 400, "message": "Cannot trade on a weekend!", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_2) == ({"code": 400, "message": "Cannot trade on a weekend!", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_1) == ({"code": 400, "message": "Cannot trade on a weekend!", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", weekend_2) == ({"code": 400, "message": "Cannot trade on a weekend!", "data": {}}, 400))       
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        # Testing that non-Forex transactions do not work at invalid times
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", pre_trading_time) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", one_min_before_trading) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", one_min_before_trading) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", midnight_check) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", pre_trading_time) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", one_min_before_trading) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", one_min_after_trading) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        assert(record_transaction_service({"action": "sell", "asset_type": "Stock (Equity)", "quantity": 2, "symbol": "aapl"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", midnight_check) == ({"code": 400, "message": "Non-Forex assets can only trade from 8:30 am to 5:00 pm! (1 hour before the market opens and upto 1 hour after the market closes)", "data": {}}, 400))       
        assert(get_asset("AAPL", 2, "Stock (Equity)") == None)
        # Testing that Forex assets can trade at some non-Forex asset invalid times
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", pre_trading_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        asset  = get_asset("EURUSD", 2, "Forex")
        assert(asset.symbol == "EURUSD")
        assert(asset.asset_type == "Forex")
        assert(asset.quantity == 2)
        assert(record_transaction_service({"action": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", pre_trading_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        asset  = get_asset("EURUSD", 2, "Forex")
        assert(asset.symbol == "EURUSD")
        assert(asset.asset_type == "Forex")
        assert(asset.quantity == 2)
        assert(record_transaction_service({"action": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 200, "message": "Success", "data": {}}, 200))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        # Check for invalid queries
        assert(record_transaction_service({"actio": "sell", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 400, "message": "Missing or incorrect query parameters", "data": {}}, 400))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "sel", "asset_type": "Forex", "quantity": 2, "symbol": "eurusd"},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 400, "message": "Invalid action", "data": {}}, 400))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        assert(record_transaction_service({"action": "buy", "asset_type": "Forex", "quantity": 2, "symbol": ""},"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDIwNTkwNSwianRpIjoiYzAxNzliZTUtNjFiNS00ZjAxLTgwZjItNGIxZmRhMDg0ODhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwidXNlcm5hbWUiOiJ0ZXN0In0sIm5iZiI6MTcwNDIwNTkwNSwiY3NyZiI6Ijk3YjcyMThiLTg0YWQtNDc0NC04NWUzLTBiNDlhNDEwNzUxZiIsImV4cCI6MTcwNDIwNjgwNX0.Uf6eODQaCqmT5dF_URHqXnc3raPnjntEI_Snm1M0dlI", post_trading_time) == ({"code": 400, "message": "Invalid Symbol", "data": {}}, 400))
        assert(get_asset("EURUSD", 2, "Forex") == None)
        