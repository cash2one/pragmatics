import os
import schedule
from threading import Thread
from flask import Flask, url_for
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

from ybsuggestions.application.apis import apis_blueprint
app.register_blueprint(apis_blueprint)

if not app.config['DEBUG']:
    from ybsuggestions.crawler.jobs import job_check_new_movies, run_schedule

    schedule.every(12).hours.do(job_check_new_movies)
    print('"Check for new movies" job scheduled, every 12 hours')
    t = Thread(target=run_schedule)
    t.start()






