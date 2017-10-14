import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://newhope_pragma:pragma566I@s39.vdl.pl/newhope_pragma'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = False