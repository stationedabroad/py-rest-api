import sqlite3

from create_app_tables import DB_NAME
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.as_json(), 200
        return {'message': 'itme not found'}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item with name {} already exists'.format(name)}, 400
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        new_item = ItemModel(name, data['price'])
        saved_item = new_item.as_json()
        new_item.create_update_item()
        return saved_item, 201
    
    def put(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return self.post(name)
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        item.price = data['price']
        item.create_update_item()
        return item.as_json(), 204

    def get_payload_parser(self, req_args: list, required=True):
	    parser = reqparse.RequestParser()
	    for arg in req_args:
	    	parser.add_argument(arg[0], type=arg[1], required=True, help=f"{arg[0]} cannot be empty!")		
	    return parser

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': 'item with name {} does not exist'.format(name)}, 400
        item.delete()
        # query = """
        #             delete from items where name = '{}'
        #         """.format(item_delete.name)
        # connection = sqlite3.connect(DB_NAME)
        # cursor = connection.cursor()
        # cursor.execute(query)

        # connection.commit()
        # connection.close()
        return {'message': 'item {} successfully deleted'.format(item.name)}, 200


class ItemList(Resource):
    def get(self):
        query = """
            select * from items;
                """
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        results = cursor.execute(query)
        items = self.format_items(results.fetchall())
        connection.commit()
        connection.close()        
        return {'items': items}, 200

    def format_items(self, items):
        item_list = []
        for item in items:
            item_list.append({'name': item[1], 'price': item[2]})
        return item_list