from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from sqldb import db

# port & debug
# env variable: FLASK_RUN_PORT=5001
# env variable: FLASK_DEBUG=1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '6565870'
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) # /auth endpointx

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
	app.run(debug=True)