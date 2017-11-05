import pytest
import asyncio
import platform
from ybsuggestions.crawler.jobs import update_imdb_info, call_imdbpy
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


def test_call_imdbpy_should_not_return_empty_output(movie_titles):
    tasks = []
    for title in range(len(movie_titles)):
        tasks.append(call_imdbpy(title))

    if platform.system() == 'Windows':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    try:
        results = loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()

    pass


def test_imdb_info_should_not_be_none_after_update(movie_titles):
    moviedaos = [MovieDAO(title) for title in movie_titles][:5]

    tasks = []
    for dao_idx in range(len(moviedaos)):
        tasks.append(update_imdb_info(moviedaos[dao_idx], dao_idx))

    if platform.system() == 'Windows':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    finally:
        loop.close()

    for dao in moviedaos:
        assert dao.imdb_info is not None
        assert dao.imdb_info[0] is not ''

#
# def test_moviedaos_should_have_movie_objects():
#
#     moviedaos = job_check_new_movies()
#
#     for dao in moviedaos:
#         assert dao.movie is not None
