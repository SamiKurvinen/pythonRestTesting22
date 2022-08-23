import hmac
from models.user import UserModel

def authenticate(username, password):
    """
    Func gets called when user calls /auth endpoint
    with username and pass
    :param username: Username as string
    :param password: unencrypted apssword as string
    :return: A UserModel objectif succesfully authenticated
    """
    
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    """
    Func gets called when user has authenticated and flask-jwt
    verified thei authorization header is correct.
    :param payload: A dict with identity key which is user_id
    :return: UserModel obj
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)