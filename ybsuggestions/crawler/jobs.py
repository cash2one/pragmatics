import platform
import os
import asyncio
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
    for dao in moviedaos:
        dao.create_movie()


# ASYNCIO JOBS


def job_check_new_movies(chunksize=0):

    moviedaos = _create_moviedaos()

    tasks = []
    for dao_idx in range(len(moviedaos)):
        tasks.append(update_imdb_info(moviedaos[dao_idx], dao_idx))

    chunks = [tasks] if not chunksize else _create_chunks(tasks, chunksize)

    for no, chunk in enumerate(chunks):
        # print('Chunk: %d' % (no + 1))
        if platform.system() == 'Windows':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(asyncio.gather(*chunk))
        finally:
            loop.close()

    _add_movies(moviedaos)

    yield moviedaos
# HELPERS


# ASYNC FUNCTIONS

async def call_imdbpy(movie_title):
    args = ["python2", "-W", "ignore",
            app.root_path + "\crawler\imdbpy_p2script.py",
            str(movie_title)]

    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE)

    stdout = await process.stdout.readline()

    if process.returncode == 0:
        print('Done! ', '(pid = ' + str(process.pid) + ')')
    else:
        print('Failed! ', '(pid = ' + str(process.pid) + ')')

    return stdout


async def update_imdb_info(moviedao, dao_idx=None):

    # if dao_idx is not None:
    #     print('Update started for idx: %d' % dao_idx)

    imdbpy_output = await call_imdbpy(moviedao.movie_title)

    imdbpy_output = imdbpy_output.decode("utf-8").strip().replace("u'", "")

    if imdbpy_output == 'IMDBFoundNothingException':
        moviedao.imdb_info = []
        if dao_idx is not None:
            print('IMDB found nothing for idx: %d' % dao_idx)

    imdb_info = imdbpy_output.split('||')
    if len(imdb_info) > 2:
        imdb_info[1] = float(imdb_info[1])
        imdb_info[2] = [g.strip(" \'") for g in imdb_info[2].strip('[]').split(',')]

    moviedao.imdb_info = imdb_info

    # if dao_idx is not None:
    #     print('Update ended for idx: %d' % dao_idx)

    return True



