from models.token_model import TokenModel
from models.user_model import UserModel

def get_user_from_token(access_token):
    """
        Retrieve a User object based on the provided access token.

        :param access_token: A string representing the access token.
        :return: User instance if a user is found with the given token, otherwise None.
        :rtype: dict
    """
    return UserModel.query.filter_by(id=TokenModel.query.filter_by(tokens=access_token).first().id).first()