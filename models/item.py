from sqldb import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))#, primary_key=True)
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def as_json(self):
        return {'name': self.name, 'price': self.price}   

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.create()      

    def delete(self):
        self.query.filter_by(name=self.name).delete()
        db.session. commit()