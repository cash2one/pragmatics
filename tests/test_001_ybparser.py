import pytest
import os
os.environ["APP_SETTINGS"] = "testing"
from ybsuggestions.crawler.ybparser import YBParser
from instance.config import Config


@pytest.fixture()
def parser():
    yb_parser = YBParser(Config.YOURBIT_MOVIES_URL)

    return yb_parser


def test_ybparser_init_raise_exception_for_none_feedurl():

    with pytest.raises(ValueError) as e:
        yb_parser = YBParser(None)
    assert "Corrupted feed url" in str(e.value)


def test_ybparser_init_raise_exception_for_empty_feedurl():

    with pytest.raises(ValueError) as e:
        yb_parser = YBParser("")
    assert "Corrupted feed url" in str(e.value)


def test_ybparser_is_inited_correctly_for_config_feedurl():

    yb_parser = YBParser(Config.YOURBIT_MOVIES_URL)

    assert yb_parser._feed_url == Config.YOURBIT_MOVIES_URL


def test_ybparser_parse_feed_returns_empty_dict_for_not_responding_feedurl():
    yb_parser = YBParser("http://shoud.not.responding.com.pl")

    feed = yb_parser.parse_feed()

    assert feed == {}


def test_ybparser_parse_feed_returns_filled_entries_from_feedurl(parser):
    feed = parser.parse_feed()

    assert feed is not None
    assert 'entries' in feed
    assert feed.entries

    for entry in feed.entries:
        assert 'title' in entry


def test_ybparser_get_torrents_titles_returns_empty_list_for_empty_entries(parser):
    feed = parser.parse_feed()
    feed.entries = []
    torrents_titles = parser.get_torrents_titles(feed)

    assert not torrents_titles


def test_ybparser_get_torrents_titles_returns_correct_titles(parser):
    feed = parser.parse_feed()
    torrents_titles = parser.get_torrents_titles(feed)

    assert torrents_titles
    for idx, title in enumerate(torrents_titles):
        assert title == feed.entries[idx]['title']


def test_ybparser_get_movies_titles_returns_some_titles(parser):
    feed = parser.parse_feed()
    torrents_titles = parser.get_torrents_titles(feed)
    movie_titles = parser.get_movies_titles(torrents_titles)

    assert len(movie_titles) > 0


def test_ybparser_remove_titles_duplicates_returns_no_duplicates():

    movies_titles = ['duplicate', 'duplicate']

    movies_titles = YBParser._remove_titles_duplicates(movies_titles)

    assert len(movies_titles) == 1
    assert movies_titles[0] == 'duplicate'