# import sqlite3
from sqldb import db

DB_NAME = 'appdata.db'

class ItemModel(db.Model):
    __tablename__ = 'items'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price=0.0):
        self.name = name
        self.price = price

    def as_json(self):
        return {'name': self.name, 'price': self.price}   

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def create_update_item(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()