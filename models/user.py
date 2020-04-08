import sqlite3

DB_NAME = 'appdata.db'

class UserModel:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('appdata.db')
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
