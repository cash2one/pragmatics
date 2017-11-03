import subprocess
import asyncio
from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.moviedao import MovieDAO, IMDBFoundNothingException
from ybsuggestions import app


def job_check_for_new_movies():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    movie_operators = [MovieDAO(title) for title in movie_titles]

    for operator in movie_operators[:1]:
        try:
            update_imdb_info(operator)
        except IMDBFoundNothingException as e:
            print(e)


async def update_imdb_info(movie_operator):
    p2_output = subprocess.check_output([
        "python2", "-W", "ignore",
        app.root_path + "\crawler\imdbpy_p2script.py",
        str(movie_operator.movie_title)], shell=True)\
        .decode("utf-8").strip().replace("u'", "")

    if p2_output == 'IMDBFoundNothingException':
        raise IMDBFoundNothingException()

    imdb_info = p2_output.split('||')
    if len(imdb_info) > 2:
        imdb_info[1] = float(imdb_info[1])
        imdb_info[2] = [g.strip(" \'") for g in imdb_info[2].strip('[]').split(',')]

    movie_operator.imdb_info = imdb_info

    return



