#!python2.7
import sys
from imdb import IMDb


def run(movie_title):
    imdb = IMDb()

    movie_list = imdb.search_movie(args[1])

    if not movie_list:
        print 'IMDBFoundNothingException'
        return

    first_match = movie_list[0]
    imdb.update(first_match)

    #('movie', 'tv series', 'tv mini series', 'video game', 'video movie', 'tv movie', 'episode')
    kind = first_match['kind']
    if kind not in ('movie', 'video movie', 'tv movie'):
        print 'IMDBFoundNothingException'
        return

    title = first_match['title']
    try:
        rating = first_match['rating']
    except KeyError:
        rating = 0.0
    try:
        genres = first_match['genre']
    except KeyError:
        genres = []
    print "%s||%f||%s" % (title, rating, genres)
    return

if  __name__ =='__main__':
    args = sys.argv
    run(args[1])
