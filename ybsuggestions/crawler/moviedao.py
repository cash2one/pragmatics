from ybsuggestions.models import Movie, Genre
from ybsuggestions import db


class IMDBFoundNothingException(Exception):
    def __init___(self, arguments):
        Exception.__init__(self, "IMDBPy found nothing using: ".format(arguments))
        self.arguments = arguments


class MovieDAO:
    def __init__(self, movie_title):
        self.movie_title = movie_title
        self.imdb_info = None
        self.movie = None

    def create_movie(self):
        if self.imdb_info:
            if self.imdb_info[0] != '':
                title = self.imdb_info[0]
                rating = self.imdb_info[1]
                genres = MovieDAO.fetch_movie_genres(self.imdb_info[2])

                self.movie = Movie(name=title, rating=rating, genres=genres)
            else:
                raise Exception('IMDB info is empty')
        else:
            raise Exception('IMDB info is missing')

    def insert_movie(self):
        if self.movie:
            db.session.add(self.movie)
            db.session.commit(self.movie)

    @staticmethod
    def fetch_movie_genres(genres_names):
        genres = []
        for genre_name in genres_names:

            genre = Genre.query.filter_by(name=genre_name).first()

            if not genre:
                genre = Genre(genre_name)
                db.session.add(genre)
                db.session.commit(genre)

            genres.append(genre)

        return genres

