import datetime
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # MAIL CONF
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # JWT CONF
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'secret-key')
    JWT_ALGORITHM = os.environ.get('JWT_SECRET', "HS256")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_VALIDATE = True
    RESTX_INCLUDE_ALL_MODELS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "postgresql://test:test$2021@psql/test"


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
    JWT_ALGORITHM = os.environ.get('JWT_SECRET', "RS256")
    JWT_PUBLIC_KEY = open('/flask/keys/jwt-key.pub', "r").read()
    JWT_PRIVATE_KEY = open('/flask/keys/jwt-key', "r").read()
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PWD = os.environ.get('DB_PWD')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PWD}@psql/{DB_NAME}"
    CELERY_BROKER_URL = 'redis://redis:6379/1',
    RESULT_BACKEND = 'redis://redis:6379/1'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
