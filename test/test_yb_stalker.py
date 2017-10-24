from yb_stalker.parser import parse_feed, get_torrents_titles, parse_torrents_titles


def test_parse_feed_should_parse_correctly():
    feed = parse_feed()

    assert feed is not None


def test_get_torrents_titles_should_return_some_titles():
    feed = parse_feed()

    torrents_titles = get_torrents_titles(feed)

    assert len(torrents_titles) > 0


def test_parse_torrents_titles_should_return_some_titles():
    feed = parse_feed()
    torrents_titles = get_torrents_titles(feed)

    movie_titles = parse_torrents_titles(torrents_titles)

    assert len(movie_titles) > 0