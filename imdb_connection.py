#!/bin/env python2.7
import sys
from imdb import IMDb


def run(movie_title):
    print movie_title
    imdb = IMDb()

    movie_list = imdb.search_movie(args[1])

    if not movie_list:
        return None

    first_match = movie_list[0]
    imdb.update(first_match)

    print first_match['rating']
    print first_match['genre']
    return first_match


if  __name__ =='__main__':
    args = sys.argv
    run(args[1])
