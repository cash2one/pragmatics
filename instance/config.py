class Config(object):
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'awdn1kj2n5n1ol!@/ai1jd9a!@#!5'
    SQLALCHEMY_DATABASE_URI = 'postgresql://newhope_movsug:movies2017prag@s39.vdl.pl'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #YOURBIT_MOVIES_URL = 'https://yourbittorrent.com/movies/rss.xml'
    YOURBIT_MOVIES_URL = 'https://rarbg.to/rssdd.php?category=movies'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/test.db'
    DEBUG = True


app_config = {
    'default': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}