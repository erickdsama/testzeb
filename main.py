import os

from flask_migrate import Migrate

from app import create_app, db

environment = os.getenv('FLASK_ENV')
if type(environment) is not str:
    environment = "default"

app = create_app(environment)
migrate = Migrate(app, db)
