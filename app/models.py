from app import db
from datetime import datetime


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    movies = db.relationship('Movie', lazy=True, backref=db.backref('genre', lazy='joined'))

    def __repr__(self):
        return '<Genre %r>' % (self.name)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),
        nullable=False)
    rating = db.Column(db.Float(2), index=True)
    date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Movie %r>' % (self.name)