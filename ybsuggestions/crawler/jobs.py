import platform
import requests
import asyncio
import schedule
import time
import sys
from flask import url_for
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.moviedao import MovieDAO
from ybsuggestions import app


def _create_moviedaos():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    moviedaos = [MovieDAO(title) for title in movie_titles]

    return moviedaos


def _create_chunks(collection, chunksize):
    for i in range(0, len(collection), chunksize):
        yield collection[i:i + chunksize]


def _add_movies(moviedaos):
    for dao_idx in range(len(moviedaos)):
        try:
            moviedaos[dao_idx].create_movie()
        except Exception as e:
            print(e)
        moviedaos[dao_idx].add_movie()


def _is_server_online():
    try:
        url = 'http://localhost:5000'
        print('Checking connection with server: %s' % url)
        r = requests.get(url)

        if r.status_code != 200:
            print('Flask server is not responding. Loop stopped.')
            return False

    except ConnectionError as e:
        print('Flask server is not responding. Loop stopped.')
        return False

    return True


def run_schedule():
    time.sleep(60)
    if not _is_server_online():
        sys.exit()

    print('Schedule started')
    while 1:
        schedule.run_pending()


# JOBS

def job_check_new_movies():
    if not _is_server_online():
        sys.exit()

    moviedaos = _create_moviedaos()

    if not moviedaos:
        print('YourBit response is empty.')
        return

    print('Movies update started')
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

    _add_movies(moviedaos)
    print('Movies update ended.')

    return


# ASYNC FUNCTIONS

async def call_imdbpy(movie_title):
    # args = ["python2", "-W", "ignore",
    #         app.root_path + "\crawler\imdbpy_p2script.py",
    #         str(movie_title)]
    #
    # process = await asyncio.create_subprocess_exec(
    #     *args, stdout=asyncio.subprocess.PIPE)

    process = await asyncio.create_subprocess_shell(
        "python2 -W ignore " + app.root_path + "\crawler\imdbpy_p2script.py '" + str(movie_title) + "'"
        , stdout=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        print('Done! ', '(pid = ' + str(process.pid) + ')')
    else:
        print('Failed! ', '(pid = ' + str(process.pid) + ')')

    return stdout.decode("utf-8").strip().replace("u'", "")


async def update_imdb_info(moviedao, dao_idx=None):

    imdbpy_output = await call_imdbpy(moviedao.movie_title)

    if imdbpy_output == 'IMDBFoundNothingException':
        moviedao.imdb_info = []
        if dao_idx is not None:
            print('IMDB found nothing for idx: %d' % dao_idx)
            return False

    imdb_info = imdbpy_output.split('||')
    if len(imdb_info) > 2:
        imdb_info[1] = float(imdb_info[1])
        imdb_info[2] = [g.strip(" \'") for g in imdb_info[2].strip('[]').split(',')]

    moviedao.imdb_info = imdb_info

    return True



