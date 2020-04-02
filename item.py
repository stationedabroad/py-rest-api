import sqlite3

from create_app_tables import DB_NAME
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    # def __init__(self, name, price):
    #     self.name = name
    #     self.price = price

    @classmethod
    def item_by_name(cls, name):
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
        return item
    
    @jwt_required()
    def get(self, name):
        item = Item.item_by_name(name)
        if item:
            return {'item': item}, 200
        return {'message': 'itme not found'}, 404
    
    def post(self, name):
        if Item.item_by_name(name):
            return {'message': 'item with name {} already exists'.format(name)}, 400
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        item, status = self.create_update_item(name, data, 'POST')
        return item, status
    
    def put(self, name):
	    parser = self.get_payload_parser([('price', float)])
	    data = parser.parse_args()
	    msg, status = self.create_update_item(name, data, 'PUT')
	    return msg, status

    def create_update_item(self, name, data, mode):
        if mode == 'POST':
            query = """
                insert into items values ('{name}', {price});
                    """
            status = 201
        if mode == 'PUT':
            query = """
                update into items values ('{name}', {price});
                    """
            status = 000
        query = query.format(name=name, price=data['price'])
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()
        connection.close()
        return {'item': 
                    {'name': name, 'price': data['price']}
               }, status

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
        return {'item': None}