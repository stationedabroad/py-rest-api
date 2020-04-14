import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel, DB_NAME

class UserRegister(Resource):
	
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str, required=True, help='username cannot be empty')
		parser.add_argument('password', type=str, required=True, help='password cannot be empty')
		data = parser.parse_args()
		
		if UserModel.find_by_username(data['username']):
			return {"error": "user already exists"}, 409

		user = UserModel(**data)
		user.create()
		
		return {"message": "user creation successful"}, 201

	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str, required=True, help='username cannot be empty')
		data = parser.parse_args()

		user = UserModel.find_by_username(data['username'])
		if user:
			return {'message': f'user {user.username} exists'}, 201	
		return {'message': 'unknown user'}, 409
