import sqlite3
from sqldb import db

DB_NAME = 'appdata.db'

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), primary_key=True)
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price=0.0):
        self.name = name
        self.price = price

    def as_json(self):
        return {'name': self.name,
                'price': self.price}   

    @classmethod
    def find_by_name(cls, name):
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
        if item:
            return cls(*item)
        return None

    def create_update_item(self, mode):
        try:
            if mode == 'POST':
                query = """
                    insert into items values ('{name}', {price});
                        """
            if mode == 'PUT':
                query = """
                    update items set price = {price}
                    where name = '{name}';
                        """
            query = query.format(name=self.name, price=self.price)
            connection = sqlite3.connect(DB_NAME)
            cursor = connection.cursor()
            cursor.execute(query)

            connection.commit()
            connection.close()
        except:
            return None
        return self