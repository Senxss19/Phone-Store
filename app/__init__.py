from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import json
import os

db = SQLAlchemy()


def init_data():
    from .models import Product

    if not Product.query.first():
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_products.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
        for row in data['phones']:
            product = Product(
                id=row['id'],
                model=row['model'],
                brand=row['brand'],
                price=row['price'],
                camera=row['camera'],
                screen_size=row['screenSize'],
                inventory=row['inventory'],
            )
            db.session.add(product)
        db.session.commit()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'test'
    app.secret_key = 'randomkey'

    db.init_app(app)

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    Bootstrap(app)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
