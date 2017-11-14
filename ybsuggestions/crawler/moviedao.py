from ybsuggestions.models import Movie, Genre
from ybsuggestions import db


class MovieDAO:
    def __init__(self, movie_title):
        if not movie_title or movie_title == '':
            raise ValueError("Corrupted movie title")

        self.movie_title = movie_title
        self.imdb_info = None
        self.movie = None

    def create_movie(self):
        if self.imdb_info:
            if set(['title', 'rating', 'genres', 'cover']) == set(self.imdb_info.keys()):
                title = self.imdb_info['title']

                if not MovieDAO.is_movie_duplicate(title):
                    rating = self.imdb_info['rating']
                    genres = MovieDAO.fetch_movie_genres(self.imdb_info['genres'])
                    cover = self.imdb_info['cover']

                    self.movie = Movie(name=title, rating=rating, genres=genres, cover=cover)
                else:
                    raise Exception('Movie already in database')
            else:
                raise AttributeError('IMDB info is corrupted')
        else:
            raise AttributeError('IMDB info is missing')

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
        genres_names = list(set(genres_names))
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

        try:
            db.session.add(genre)
            db.session.commit()

            print('New genre added to database: %s(#%d)' % (genre.name, genre.id))
            return genre
        except Exception as e:
            print('Genre already in database:', e)

        return None
