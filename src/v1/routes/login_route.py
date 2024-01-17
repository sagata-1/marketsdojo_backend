@login_route.route("/v1/api/login", methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)