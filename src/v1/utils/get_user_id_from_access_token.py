# Desc: Returns user_id from access_token using SQL query
def get_user_id_from_access_token(access_token):
    try:
        user_id=tokens_model.query.filter_by(token=access_token).first().user_id
        return user_id
    except:
        return None