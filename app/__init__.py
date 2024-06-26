from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "hello"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users1.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import init_app as routes_init_app
    routes_init_app(app)
    
    # Optionally create database tables if needed
    with app.app_context():
        db.create_all()

    return app
