from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "diplodocus.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Diplodocus'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from api.models import JobOffer

    with app.app_context():
        create_database(app)

    return app


def create_database(app):
    if not path.exists('api/' + DB_NAME):
        db.create_all()
        print('Database created!')