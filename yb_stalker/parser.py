import feedparser
from config import YOURBIT_MOVIES_URL
from ptn import ptn

def parse_feed():
    try:
        feed = feedparser.parse(YOURBIT_MOVIES_URL)
    except Exception as e:
        print('Feedparser error' + e)

    return feed


def get_torrents_titles(feed):
    torrents_titles = []
    for entry in feed.entries:
        torrent_title = entry.title
        torrents_titles.append(torrent_title)

    return torrents_titles


def parse_torrents_titles(torrents_titles):
    movies_titles = []
    for t_title in torrents_titles:
        m_title = ptn.parse(t_title)
        movies_titles.append(m_title)

    return movies_titles