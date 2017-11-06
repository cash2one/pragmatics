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
            if len(self.imdb_info) == 3:
                title = self.imdb_info[0]

                if not MovieDAO.is_movie_duplicate(title):
                    rating = self.imdb_info[1]
                    genres = MovieDAO.fetch_movie_genres(self.imdb_info[2])

                    self.movie = Movie(name=title, rating=rating, genres=genres)
                else:
                    raise Exception('Movie already in database')
            else:
                raise Exception('IMDB info is empty')
        else:
            raise Exception('IMDB info is missing')

    def add_movie(self):
        if self.movie:
            db.session.add(self.movie)
            db.session.commit()
            db.session.flush()

            print('New movie added to database: %s(#%d)' % (self.movie.name, self.movie.id))

    @staticmethod
    def is_movie_duplicate(movie_title):
        movie = Movie.query.filter_by(name=movie_title).first()

        return True if movie else False

    @staticmethod
    def fetch_movie_genres(genres_names):
        genres = []
        for genre_name in genres_names:

            genre = Genre.query.filter_by(name=genre_name).first()

            if not genre:
                genre = MovieDAO.add_genre(genre_name)

            genres.append(genre)

        db.session.flush()

        return genres

    @staticmethod
    def add_genre(genre_name):
        genre = Genre(name=genre_name)
        db.session.add(genre)
        db.session.commit()

        print('New genre added to database: %s(#%d)' % (genre.name, genre.id))
        return genre

