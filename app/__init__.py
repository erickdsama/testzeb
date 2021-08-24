from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
api_ = Api(doc='/docs')
jwt_manager = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config['default'].init_app(app)
    db.init_app(app)
    api_.init_app(app)
    from app.api import api_bp
    app.register_blueprint(api_bp)
    jwt_manager.init_app(app)
    return app
