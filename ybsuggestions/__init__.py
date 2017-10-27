from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from ybsuggestions.application.views import application_blueprint

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from ybsuggestions import models

migrate = Migrate(app, db)

app.register_blueprint(application_blueprint)