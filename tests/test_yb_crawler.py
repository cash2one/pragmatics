from ybsuggestions.crawler.helpers import YBParser
from ybsuggestions import app


def test_parse_feed_should_parse_correctly():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])

    feed = yb_parser.parse_feed()

    assert feed is not None


def test_get_torrents_titles_should_return_some_titles():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()

    torrents_titles = yb_parser.get_torrents_titles(feed)

    assert len(torrents_titles) > 0


def test_parse_torrents_titles_should_return_some_titles():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    assert len(movie_titles) > 0