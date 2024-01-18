from test_login_service import app, login_api

def test_login():
    with app.app_context():
        assert(login_api({"email":"ajasuja1@jhu.edu", "password": "abcdefg"}) == ({"username":"Arman Jasuja", "user_id": 26, "email": "ajasuja1@jhu.edu", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6IkFybWFuIEphc3VqYSIsImlhdCI6MTcwNDE5MDI5MiwianRpIjoiMWI4N2Q1OTQtNWVkMy00ZDk3LWEzNTAtMGJlMzhlOTU4NzA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjYsIm5iZiI6MTcwNDE5MDI5MiwiY3NyZiI6IjBlNTBjMTZjLTNjMWItNDY0Ny1hYWFlLTgwMDY3OTdiYWU2YSIsImV4cCI6MTcwNDE5MTE5Mn0.WC6XDZs3tVyEHT8y3WN0SVxEUVkAoBdKKCmfzF6OVlk"}, 200))
        assert(login_api({"email":"ajasuja1@jhu.edu", "password": "abcdef"}) == ({"error": {"code": 403, "message": "Incorrect email and/or password"}}, 403))
        assert(login_api({"emai":"ajasuja1@jhu.edu", "password": "abcdefg"}) == ({"error": {"code": 403, "message": "email not provided"}}, 403))
        assert(login_api({"email":"ajasuja1@jhu.edu", "passwor": "abcdefg"}) == ({"error": {"code": 403, "message": "Did not enter a password"}}, 403))