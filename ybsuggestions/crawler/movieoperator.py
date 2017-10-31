from ybsuggestions.models import Movie, Genre
from ybsuggestions import db


class MovieOperator:
    def __init__(self, movie_title):
        self.movie_title = movie_title
        self.imdb_info = None
        self.movie = None

    def build_movie(self):
        if self._imdb_info:
            title = self._imdb_info['title']
            genre = self._imdb_info['genre']
            rate = self._imdb_info['rate']

            self.movie = Movie(name=title, genre_id=genre.id, rating=rate)
        else:
            raise Exception('IMDB info is missing')

    def insert_movie(self):
        if self.movie:
            db.session.add(self.movie)
            db.session.commit(self.movie)

    @staticmethod
    def fetch_movie_genre(genre_name):
        genre = Genre.query.filter_by(name=genre_name).first()

        if not genre:
            genre = Genre(genre_name)
            db.session.add(genre)
            db.session.commit(genre)

        return genre

