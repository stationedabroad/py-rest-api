from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [

]

# port
# env variable: FLASK_RUN_PORT=5001
# env variable: FLASK_DEBUG=1


class Item(Resource):
	def get(self, name):
		item = next(filter(lambda n: n['name'] == name, items), None)
		if item:
			return {'item': item}, 200
		return {'item': item}, 404

	def post(self, name):
		item = next(filter(lambda n: n['name'] == name, items), None)
		if item:
			return {'item': f'{name} already exists'}, 403
		data = request.get_json() # silent=True or force=True
		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201

	def put(self):
		pass		

class ItemList(Resource):
	def get(self):
		if items:
			return items, 200
		return {'items': None}, 404


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
	app.run(debug=True)