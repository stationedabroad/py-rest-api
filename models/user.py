import sqlite3
from sqldb import db

DB_NAME = 'appdata.db'

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(20))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	def create(self):
		db.session.add(self)		
		db.session.commit()

	def update(self):
		self.create()

	def delete(self):
		self.query.filter_by(username=self.username).delete()
		db.session.commit()