import pytest
import os
import asyncio
import platform
os.environ["APP_SETTINGS"] = "testing"
from ybsuggestions.crawler.jobs import _create_moviedaos, update_imdb_info, \
    job_check_new_movies, _is_server_online, call_imdbpy
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions.crawler.ybparser import YBParser
from instance.config import Config


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


def test_jobs_call_imdbpy_returns_exception_message_for_empty_movie_title(loop):

    try:
        imdbpy_return = loop.run_until_complete(call_imdbpy(''))
    finally:
        loop.close()

    assert 'IMDBFoundNothingException' in imdbpy_return


def test_jobs_call_imdbpy_returns_exception_message_for_unrecognised_movie_title(loop):

    try:
        imdbpy_return = loop.run_until_complete(call_imdbpy('123!@#!@#dawdaw'))
    finally:
        loop.close()

    assert 'IMDBFoundNothingException' in imdbpy_return


def test_jobs_call_imdbpy_returns_valid_info_for_private_rayan(loop):

    try:
        imdbpy_return = loop.run_until_complete(call_imdbpy('Private Ryan'))
    finally:
        loop.close()

    assert 'Saving Private Ryan||8' in imdbpy_return


def test_jobs_update_imdb_info_returns_false_for_moviedao_with_unrecognised_movie_title(loop):
    movie_title = '123!@#!@#dawdaw'
    moviedao = MovieDAO(movie_title)

    try:
        result = loop.run_until_complete(update_imdb_info(moviedao))
    finally:
        loop.close()

    assert not result
    assert len(moviedao.imdb_info) == 0


def test_jobs_update_imdb_info_returns_true_for_private_rayan_moviedao(loop):
    movie_title = 'Private Ryan'
    moviedao = MovieDAO(movie_title)

    try:
        result = loop.run_until_complete(update_imdb_info(moviedao))
    finally:
        loop.close()

    assert result
    assert len(moviedao.imdb_info) == 4
    assert 'Saving Private Ryan' in moviedao.imdb_info[0]
    assert moviedao.imdb_info[1] > 8.0
    assert len(moviedao.imdb_info[2]) > 1


def test_jobs_job_check_new_movies_exits_during_tests():

    with pytest.raises(SystemExit) as e:
        job_check_new_movies()
    assert type(e.value) == SystemExit


