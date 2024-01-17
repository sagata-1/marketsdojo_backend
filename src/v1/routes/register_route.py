@register_route.route("/v1/api/register", methods=['POST'])
def register():
    data = request.get_json()
    return register_service(data)