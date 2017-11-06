SECRET_KEY = 'awdn1kj2n5n1ol!@/ai1jd9a!@#!5'

SQLALCHEMY_DATABASE_URI = "sqlite:///..\\app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

YOURBIT_MOVIES_URL = 'https://yourbittorrent.com/movies/rss.xml'

JOBS = [
    {
        'id': 'job1',
        'func': 'ybsuggestions.crawler.jobs:job',
        'args': (1, 2),
        'trigger': 'interval',
        'seconds': 10
    }
]

SCHEDULER_API_ENABLED = True