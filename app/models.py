from . import db
from flask_login import UserMixin
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(200), nullable=False, unique=True)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    camera = db.Column(db.String(200), nullable=False)
    screen_size = db.Column(db.Float, default=0, nullable=False)
    inventory = db.Column(db.Integer, default=0, nullable=False)


class User(UserMixin, db.Model):
    def get_id(self):
        return self.id

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    nickname = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'),  nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'),
                        nullable=False)
