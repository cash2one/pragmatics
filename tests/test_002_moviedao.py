import pytest
import os
os.environ["APP_SETTINGS"] = "testing"
from datetime import datetime
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.models import Movie
from instance.config import Config


@pytest.fixture()
def parser():
    yb_parser = YBParser(Config.YOURBIT_MOVIES_URL)

    return yb_parser


@pytest.fixture()
def movie_titles(parser):
    feed = parser.parse_feed()
    torrents_titles = parser.get_torrents_titles(feed)

    movie_titles = parser.get_movies_titles(torrents_titles)

    return movie_titles


@pytest.fixture()
def moviedao():
    movie_title = datetime.now().strftime("Title %Y-%m-%d %H:%M:%S.%f")
    moviedao = MovieDAO(movie_title)

    return moviedao


@pytest.fixture()
def moviedao_movie(moviedao):
    moviedao.movie = Movie(name=moviedao.movie_title)

    return moviedao


def test_moviedao_init_raise_exception_for_none_title():
    with pytest.raises(ValueError) as e:
        moviedao = MovieDAO(None)
    assert "Corrupted movie title" in str(e.value)


def test_moviedao_init_raise_exception_for_empty_title():
    with pytest.raises(ValueError) as e:
        moviedao = MovieDAO('')
    assert "Corrupted movie title" in str(e.value)


def test_moviedao_add_genre_returns_object_with_id():
    genre_name = datetime.now().strftime("Test %Y-%m-%d %H:%M:%S.%f")

    genre = MovieDAO.add_genre(genre_name)

    assert genre.id


def test_moviedao_add_genre_returns_none_for_duplicate():
    genre_name = datetime.now().strftime("Test %Y-%m-%d %H:%M:%S.%f")

    MovieDAO.add_genre(genre_name)
    genre = MovieDAO.add_genre(genre_name)

    assert not genre


def test_moviedao_fetch_movie_genres_returns_objects_with_ids_related_to_given_names():
    genres_names = []
    for i in range(10):
        genres_names.append(str(i) + 'Test ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

    genres = MovieDAO.fetch_movie_genres(genres_names)

    for genre in genres:
        assert genre.id


def test_moviedao_fetch_movie_genres_returns_not_duplicated_objects():
    genre_name = datetime.now().strftime("Test %Y-%m-%d %H:%M:%S.%f")
    genres_names = [genre_name, genre_name]

    genres = MovieDAO.fetch_movie_genres(genres_names)

    assert len(genres) == 1


def test_moviedao_add_movie_updates_objects_id(moviedao_movie):
    moviedao_movie.add_movie()

    assert moviedao_movie.movie.id


def test_moviedao_is_movie_duplicate_returns_true_for_duplicate(moviedao_movie):
    moviedao_movie.add_movie()

    assert MovieDAO.is_movie_duplicate(moviedao_movie.movie.name)


def test_moviedao_is_movie_duplicate_returns_false_for_new_title():
    movie_title = datetime.now().strftime("Movie %Y-%m-%d %H:%M:%S.%f")

    assert not MovieDAO.is_movie_duplicate(movie_title)


def test_moviedao_create_movie_creates_object_for_valid_imdb_info(moviedao):
    imdb_info = [moviedao.movie_title, 5.0, ['Drama', 'Horror'], '']
    moviedao.imdb_info = imdb_info

    moviedao.create_movie()

    assert moviedao.movie
    assert moviedao.movie.name == imdb_info[0]
    assert moviedao.movie.rating == imdb_info[1]
    for genre in moviedao.movie.genres:
        assert genre.name in imdb_info[2]
    assert moviedao.movie.cover == imdb_info[3]


def test_moviedao_create_movie_raise_exception_for_imdb_info_with_title_duplicate(moviedao_movie):
    moviedao_movie.add_movie()

    imdb_info = [moviedao_movie.movie_title, 5.0, ['Drama', 'Horror'], '']
    moviedao_movie.imdb_info = imdb_info

    with pytest.raises(Exception) as e:
        moviedao_movie.create_movie()
    assert "Movie already in database" in str(e.value)


def test_moviedao_create_movie_raise_exception_for_corrupted_imdb_info(moviedao):
    imdb_info = [5.0, '']
    moviedao.imdb_info = imdb_info

    with pytest.raises(AttributeError) as e:
        moviedao.create_movie()
    assert "IMDB info is corrupted" in str(e.value)


def test_moviedao_create_movie_raise_exception_for_empty_imdb_info(moviedao):
    imdb_info = []
    moviedao.imdb_info = imdb_info

    with pytest.raises(AttributeError) as e:
        moviedao.create_movie()
    assert "IMDB info is missing" in str(e.value)



