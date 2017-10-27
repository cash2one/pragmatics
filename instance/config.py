SQLALCHEMY_DATABASE_URI = 'postgresql://newhope_movies:pragma566I@s39.vdl.pl/newhope_movies'
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