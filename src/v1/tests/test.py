import test_login_service
from test_login_service import login_api
import test_portfolio_service
from test_portfolio_service import portfolio_service

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
                