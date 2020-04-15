from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.as_json(), 200
        return {'message': 'store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'store already exists'}, 400
        store = StoreModel(name)
        try:
            store.create()
        except:
            return {'message': 'error occurred while creating the store'}, 500
        
        return store.as_json(), 201
        

    def delete(self, name):
        store = StoreModel(name)
        if store:
            try:
                store.delete()
            except:
                return {'message': 'error deleting the store'}, 500
        return {'message': 'store removed successfully'}, 201

class StoreList(Resource):
    def get(self):                
        return {'stores': list(map(lambda store: store.as_json(), StoreModel.query.all()))}, 200