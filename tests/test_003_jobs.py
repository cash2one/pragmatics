import pytest
import asyncio
from ybsuggestions.crawler.jobs import update_imdb_info
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.moviedao import MovieDAO, IMDBFoundNothingException
from ybsuggestions import app


@pytest.fixture()
def movie_titles():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    return movie_titles


def test_imdb_info_update_should_be_fetched_correctly(movie_titles):
    movie_operators = [MovieDAO(title) for title in movie_titles]

    loop = asyncio.get_event_loop()
    tasks = []
    for o_idx in range(len(movie_operators)):
        tasks.append(update_imdb_info(movie_operators[o_idx]))

    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except IMDBFoundNothingException:
        print('IMDB found nothing')

    loop.close()

    pass

