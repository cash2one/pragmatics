import os
from threading import Thread
import asyncio
import platform
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
try:
    app.config.from_object(app_config[os.getenv('APP_SETTINGS', 'default')])
    print('Settings loaded for:', os.getenv('APP_SETTINGS', 'default'))
except KeyError as e:
    app.config.from_object(app_config['default'])
    print('Settings key not found:', e, '. Default Config loaded.')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from ybsuggestions import models
from ybsuggestions import forms

migrate = Migrate(app, db)

from ybsuggestions.application.views import application_blueprint
app.register_blueprint(application_blueprint)

import ybsuggestions.application.apis
from ybsuggestions.crawler.jobs import job_check_new_movies


@app.before_first_request
def run_movies_updater():
    if not app.config['DEBUG']:
        print('Movies update loop started')

        try:
            t = Thread(target=job_check_new_movies)
            t.start()
        except KeyboardInterrupt as e:
            print('Thread interrupted:', e)





