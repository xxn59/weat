from . import db
from sqlalchemy.types import Enum

cuisine = db.Table('cuisine',
                   db.Column('salad_id', db.Integer, db.ForeignKey('salad.id')),
                   db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
                   )

salad_order_table = db.Table('salad_order_table',
                   db.Column('salad_id', db.Integer, db.ForeignKey('salad.id')),
                   db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
                   )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    floor = db.Column(db.Integer, default=23)
    cell = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    level = db.Column(db.Integer, db.ForeignKey('userlevel.level_num'))
    group = db.Column(db.String(20))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.level == 5

    def is_provider(self):
        return self.level == 3

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def add_order(self, order):
        self.orders.append(order)
        return self

    def del_order(self, order):
        self.orders.remove(order)
        return self

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Userlevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    level_num = db.Column(db.Integer, default=1)
    user = db.relationship('User', backref='clearance', lazy='dynamic')


meals = ('breakfast', 'lunch', 'dinner')
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, default=0)
    cos_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    salads = db.relationship('Salad', backref='including_order', lazy='dynamic')
    meal = db.Column(db.Enum, Enum(*meals))
    remark = db.Column(db.String(140))

    def add_salad(self, salad):
        self.salads.append(salad)
        return self

    def del_salad(self, salad):
        self.salads.remove(salad)
        return self


    def __repr__(self):
        return '<Order %r>' % (self.body)



class Salad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True)
    name_zh = db.Column(db.String(40))
    price = db.Column(db.Integer, default=0)
    foods = db.relationship('Food', secondary=cuisine)
    status = db.Column(db.Integer, default=1)
    description = db.Column(db.String(140))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def add_food(self, food):
        self.foods.append(food)
        return self

    def del_food(self, food):
        self.foods.remove(food)
        return self

    def including(self, food):
        return self

    def __repr__(self):
        return '<Post %r>' % (self.body)

food_category = ('vegetable', 'meat', 'sauce', 'premium', 'new_arrival')
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True)
    price = db.Column(db.Integer, default=0)
    cat = db.Column(db.Enum, Enum(*food_category))
    salads = db.relationship('Salad', secondary=cuisine)


    def __unicode__(self):
        return self.name