from ybsuggestions.crawler.jobs import update_imdb_info
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.movieoperator import MovieOperator
from ybsuggestions import app


def test_imdb_info_update_should_be_fetched_correctly():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    movie_operators = [MovieOperator(title) for title in movie_titles]

    for operator in movie_operators:
        update_imdb_info(operator)