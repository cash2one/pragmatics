import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://newhope_movies:pragma566I@s39.vdl.pl/newhope_movies'
SQLALCHEMY_TRACK_MODIFICATIONS = False

YOURBIT_MOVIES_URL = 'https://yourbittorrent.com/movies/rss.xml'