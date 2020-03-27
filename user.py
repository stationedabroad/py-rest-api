import sqlite3
from flask_restful import Resource, reqparse

DB_NAME = 'appdata.db'

class User:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()
		
		query = "select * from users where username = \"{}\"".format(username)
		results = cursor.execute(query)
		user = results.fetchone()
		connection.close()
		if user:
			return cls(*user)
		return None

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()
		
		query = "select * from users where id = \"{}\"".format(_id)
		results = cursor.execute(query)
		user = results.fetchone()
		connection.close()
		if user:
			return cls(*user)
		return None

class UserRegister(Resource):
	def post(self):
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