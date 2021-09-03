from user import User
from werkzeug.security import safe_str_cmp
users = [User(1,'allen', 'allen1234')]

def authenticate(username:str, password:str):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    print(payload)
    user_id = payload['identity']
    return User.find_by_id(user_id)