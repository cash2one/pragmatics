import pytest
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.jobs import update_imdb_info
from ybsuggestions import app


@pytest.fixture()
def movie_titles():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    return movie_titles


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


