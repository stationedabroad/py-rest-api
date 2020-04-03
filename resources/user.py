import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel

DB_NAME = 'appdata.db'

class UserRegister(Resource):
	def post(self):

		if UserModel.find_by_username(data['username']):
			return {"error": "user already exists"}, 409

		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()

		parser = reqparse.RequestParser()
		parser.add_argument('username', type=str, required=True, help='username cannot be empty')
		parser.add_argument('password', type=str, required=True, help='password cannot be empty')
		data = parser.parse_args()

		
		query = "insert into users(username, password) values (?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()
		
		return {"message": "user creation successful"}, 201