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
    rating = db.Column(db.Float(2))
    genres = db.relationship('Genre', secondary=movie_genres,
                                lazy='subquery',
                                backref=db.backref('genres', lazy=True))
    cover = db.Column(db.String(256), nullable=True)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)

    def __repr__(self):
        return '<Movie %r>' % (self.name)

    def to_json(self):
        return {'id': self.id,
                'title': self.name,
                'rating': self.rating,
                'cover': self.cover,
                'genres': {genre.id: genre.name for genre in self.genres}}


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
    name = db.Column(db.String(128), nullable=False)
    min_rating = db.Column(db.Float(2))
    whitelist = db.relationship('Genre', secondary=profile_whitelist,
                                lazy='subquery',
                                backref=db.backref('whitelist', lazy=True))
    blacklist = db.relationship('Genre', secondary=profile_blacklist,
                                lazy='subquery',
                                backref=db.backref('blacklist', lazy=True))
    rated_suggestions = db.relationship('ProfileSuggestion', backref='profile', lazy=True)

    def __repr__(self):
        return '<Profile %r>' % (self.name)


class ProfileSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    was_liked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<ProfileSuggestion %r>' % (self.id)