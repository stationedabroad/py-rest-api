import sqlite3

from create_app_tables import DB_NAME
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    # def __init__(self, name, price):
    #     self.name = name
    #     self.price = price
    
    @jwt_required()
    def get(self, name):
        print("entered!!!")
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        query = """
            select * 
            from items
            where name = '{item_name}';
        """.format(item_name=name)
        result = cursor.execute(query)
        item = result.fetchone()
        connection.close()

        if item:
            return {'item': item}, 200
        return {'message': 'itme not found'}, 404
    
    def post(self, name):
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        msg, status = self.create_update_item(name, data, 'POST')
        return msg, status
    
    def put(self, name):
	    parser = self.get_payload_parser([('price', float)])
	    data = parser.parse_args()
	    msg, status = self.create_update_item(name, data, 'PUT')
	    return msg, status

    def create_update_item(self, name, data, mode):
	    item = next(filter(lambda n: n['name'] == name, items), None)
        # if item:
        #     if mode == 'PUT':
		#     	item.update(data)
		# 	    return {'item': f'{name} updated with price'}, 200
    	# 	if mode == 'POST':
	    # 		return {'item': f'{name} already exists'}, 403				
    	# item = {'name': name, 'price': data['price']}
	    # items.append(item)
    	# return item, 201		

    def get_payload_parser(self, req_args: list, required=True):
	    parser = reqparse.RequestParser()
	    for arg in req_args:
	    	parser.add_argument(arg[0], type=arg[1], required=True, help=f"{arg[0]} cannot be empty!")		
	    return parser

    def delete(self, name):
        pass
		# global items
		# items = list(filter(lambda n: n['name'] != name, items))
		# return {'item': f'{name} item deleted'}, 200


class ItemList(Resource):
	def get(self):
		if items:
			return items, 200
		return {'items': None}, 404