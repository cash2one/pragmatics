import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
try:
    app.config.from_object(app_config[os.getenv('APP_SETTINGS', 'default')])
except KeyError as e:
    print('Settings key not found:', e, '. Default Config loaded.')
    app.config.from_object(app_config['default'])
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from ybsuggestions import models
from ybsuggestions import forms

migrate = Migrate(app, db)

from ybsuggestions.application.views import application_blueprint
app.register_blueprint(application_blueprint)

import ybsuggestions.application.apis