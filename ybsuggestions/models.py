from ybsuggestions import db
from datetime import datetime


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    movies = db.relationship('Movie', lazy=True,
                             backref=db.backref('genre', lazy='joined'))

    def __repr__(self):
        return '<Genre %r>' % (self.name)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),
                         nullable=False)
    rating = db.Column(db.Float(2), index=True)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)

    def __repr__(self):
        return '<Movie %r>' % (self.name)


profile_whitelist = db.Table('profile_whitelist',
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genre.id'),
                                       primary_key=True),
                             db.Column('profile_id', db.Integer,
                                       db.ForeignKey('profile.id'),
                                       primary_key=True)
                             )

profile_blacklist = db.Table('profile_blacklist',
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genre.id'),
                                       primary_key=True),
                             db.Column('profile_id', db.Integer,
                                       db.ForeignKey('profile.id'),
                                       primary_key=True)
                             )


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    whitelist = db.relationship('Genre', secondary=profile_whitelist,
                                lazy='subquery',
                                backref=db.backref('whitelist', lazy=True))
    blacklist = db.relationship('Genre', secondary=profile_whitelist,
                                lazy='subquery',
                                backref=db.backref('blacklist', lazy=True))

    def __repr__(self):
        return '<Profile %r>' % (self.name)
