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
        return {'message': 'item not found'}, 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item with name {} already exists'.format(name)}, 400
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        new_item = ItemModel(name, data['price'])
        new_item.create()
        saved_item = ItemModel.find_by_name(name)
        return saved_item.as_json(), 201
    
    def put(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return self.post(name)
        parser = self.get_payload_parser([('price', float)])
        data = parser.parse_args()
        item.price = data['price']
        item.update()
        updated_item = ItemModel.find_by_name(name)
        return updated_item.as_json(), 204

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
        items = [item.as_json() for item in ItemModel.query.all()]
        return {'items':items }, 200