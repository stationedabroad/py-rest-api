from sqldb import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price=0.0):
        self.name = name

    def as_json(self):
        return {'name': self.name, 'items': list(map(lambda item: item.as_json(), self.items.all()))}   

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