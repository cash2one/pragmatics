import feedparser
from ptn import ptn


class YBParser:
    def __init__(self, feed_url):
        self._feed_url = feed_url

    def parse_feed(self):
        try:
            feed = feedparser.parse(self._feed_url)
        except Exception as e:
            print('Feedparser error' + e)

        return feed

    @staticmethod
    def get_torrents_titles(feed):
        torrents_titles = []
        for entry in feed.entries:
            torrent_title = entry.title
            torrents_titles.append(torrent_title)

        return torrents_titles

    @staticmethod
    def get_movies_titles(torrents_titles):
        movies_titles = []
        for t_title in torrents_titles:
            m_title = ptn.parse(t_title)
            movies_titles.append(m_title)

        return movies_titles
