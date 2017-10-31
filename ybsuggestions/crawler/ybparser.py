import feedparser
from ptn import ptn


class YBParser:
    def __init__(self, feed_url):
        self._feed_url = feed_url

    @staticmethod
    def _remove_titles_duplicates(movie_titles):
        return list(set(movie_titles))

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
        for title in torrents_titles:
            movie_info = ptn.parse(title)

            if 'title' in movie_info:
                if movie_info['title'] != '':
                    movies_titles.append(movie_info['title'])

        return YBParser._remove_titles_duplicates(movies_titles)
