from ybsuggestions.crawler.movieoperator import MovieOperator
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions import app


def test_movies_operators_are_inited_correctly():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    movie_operators = [MovieOperator(title) for title in movie_titles]

    assert len(movie_titles) == len(movie_operators)

    for i, operator in enumerate(movie_operators):
        assert operator.movie_title == movie_titles[i]
        assert not operator.imdb_info
        assert not operator.movie


