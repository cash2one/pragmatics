from ybsuggestions import db
from datetime import datetime


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)

    def __repr__(self):
        return '<Genre %r>' % (self.name)


movie_genres = db.Table('movie_genres',
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genre.id'),
                                       primary_key=True),
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movie.id'),
                                       primary_key=True)
                             )


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    rating = db.Column(db.Float(2), index=True)
    genres = db.relationship('Genre', secondary=movie_genres,
                                lazy='subquery',
                                backref=db.backref('genres', lazy=True))
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)

    def __repr__(self):
        return '<Movie %r>' % (self.name)

    def to_json(self):
        return {'id': self.id,
                'title': self.name,
                'rating': self.name,
                'genres_ids': [genre.id for genre in self.genres]}

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
