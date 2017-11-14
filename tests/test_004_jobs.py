import pytest
import os
import asyncio
import platform
os.environ["APP_SETTINGS"] = "testing"
os.environ["HOST_URL"] = "http://127.0.0.1:80"
from ybsuggestions.crawler.jobs import _create_moviedaos, update_imdb_info, \
    job_check_new_movies, _is_server_online
from ybsuggestions.crawler.moviedao import MovieDAO


@pytest.fixture()
def loop():
    if platform.system() == 'Windows':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop


def test_jobs_create_moviedaos_init_moviedaos_correctly():
    moviedaos = _create_moviedaos()

    for moviedao in moviedaos:
        assert moviedao.movie_title


def test_jobs_is_server_online_returns_false_during_tests():

    assert not _is_server_online()


def test_jobs_update_imdb_info_returns_false_for_moviedao_with_unrecognised_movie_title(loop):
    movie_title = '123!@#!@#dawdaw'
    moviedao = MovieDAO(movie_title)

    try:
        result = loop.run_until_complete(update_imdb_info(moviedao))
    finally:
        loop.close()

    assert not result
    assert not moviedao.imdb_info


def test_jobs_update_imdb_info_returns_true_for_private_rayan_moviedao(loop):
    movie_title = 'Private Ryan'
    moviedao = MovieDAO(movie_title)

    try:
        result = loop.run_until_complete(update_imdb_info(moviedao))
    finally:
        loop.close()

    assert result
    assert moviedao.imdb_info
    assert 'title' in moviedao.imdb_info
    assert 'Saving Private Ryan' in moviedao.imdb_info['title']
    assert 'rating' in moviedao.imdb_info
    assert moviedao.imdb_info['rating'] > 8.0
    assert 'genres' in moviedao.imdb_info
    assert len(moviedao.imdb_info['genres']) > 1


