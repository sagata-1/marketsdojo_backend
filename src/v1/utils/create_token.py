from flask_jwt_extended import create_access_token

def create_token(user_id, username):
    """
    Create a token for a user.

    Inputs:
    user_id (int): The id of the user.
    username (str): The users username

    Output:
    access_token (str): the access token generated from the user id and username of the user.
    """
    access_token = create_access_token(identity={'id': user_id, 'username': username}, expires_delta=None)
    return access_token