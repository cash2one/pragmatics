import pytest
import os
from datetime import datetime
os.environ["APP_SETTINGS"] = "testing"
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.jobs import update_imdb_info
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


def test_moviedaos_are_inited_correctly(movie_titles):
    moviedaos = [MovieDAO(title) for title in movie_titles]

    assert len(movie_titles) == len(moviedaos)

    for i, operator in enumerate(moviedaos):
        assert operator.movie_title == movie_titles[i]
        assert not operator.imdb_info
        assert not operator.movie


def test_moviedaos_should_have_movie_objects(movie_titles):
    moviedaos = [MovieDAO(title) for title in movie_titles]

    for dao_idx in range(len(moviedaos)):
        update_imdb_info(moviedaos[dao_idx], dao_idx)

    pass



#testy: dodawanie, update, sprawdzenie unikatu, odrzucenie dodawania gdy imdb niekompletne


