from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note')
    orders = db.relationship('Order')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.String())
    rating = db.Column(db.Integer())
    price = db.Column(db.Integer())
    qty = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_qty = db.Column(db.Integer())
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    # amount = db.Column(db.Integer())


# class OrderLine(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     order_qty = db.Column(db.Integer())



