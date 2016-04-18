from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    floor = db.Column(db.Integer, default=23)
    cell = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    cos_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    salads = db.relationship('Salad', backref='including_order', lazy='dynamic')

    def __repr__(self):
        return '<Order %r>' % (self.body)

cuisine = db.Table('cuisine',
                   db.Column('salad_id', db.Integer, db.ForeignKey('salad.id')),
                   db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
                   )

class Salad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True)
    name_zh = db.Column(db.String(40))
    price = db.Column(db.Integer, default=0)
    components = db.relationship('Food', secondary=cuisine, backref='salads', lazy='dynamic')
    description = db.Column(db.String(140))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True)
    price = db.Column(db.Integer, default=0)


    def __unicode__(self):
        return self.name