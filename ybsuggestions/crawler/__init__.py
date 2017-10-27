from ybsuggestions import app
from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)