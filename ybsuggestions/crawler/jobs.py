import subprocess

from ybsuggestions.crawler.ybparser import YBParser
from ybsuggestions.crawler.movieoperator import MovieOperator
from ybsuggestions import app


def job_check_for_new_movies():
    yb_parser = YBParser(app.config['YOURBIT_MOVIES_URL'])
    feed = yb_parser.parse_feed()
    torrents_titles = yb_parser.get_torrents_titles(feed)

    movie_titles = yb_parser.get_movies_titles(torrents_titles)

    for title in movie_titles:
        movie = MovieOperator(title)


def update_imdb_info(movie_operator):
    completed = subprocess.run(["py", "-2.7", "C:\ITStuff\Projects\pragmatics\imdb_connection.py", str(movie_operator.movie_title)], check=True)

    pass
        # return first_match

    # return {'title': first_match['title'], 'genre': first_match['drama'], 'rate': float(first_match['rating'])}



