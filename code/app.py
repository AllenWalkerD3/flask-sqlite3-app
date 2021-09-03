from user import UserRegister
from security import authenticate, identity

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

app = Flask(__name__)
app.secret_key = "secret_key"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
from item import Item, ItemList


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
