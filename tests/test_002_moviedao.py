import pytest
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions import app


@pytest.fixture()
def movie_titles():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    return movie_titles


def test_movies_operators_are_inited_correctly(movie_titles):
    movie_operators = [MovieDAO(title) for title in movie_titles]

    assert len(movie_titles) == len(movie_operators)

    for i, operator in enumerate(movie_operators):
        assert operator.movie_title == movie_titles[i]
        assert not operator.imdb_info
        assert not operator.movie


#testy: dodawanie, update, sprawdzenie unikatu, odrzucenie dodawania gdy imdb niekompletne


