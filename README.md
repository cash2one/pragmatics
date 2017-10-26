## Python Task Description:
Mini-service suggesting movies to download from torrents

###### Tech requirements:
- setuptools
- docker
- db of choice (postgresql/mysql/mongo/couchdb)
- use imdbpy source (http://imdbpy.sourceforge.net/) to figure out IMDB api you need (please mind that this library will not work for Python 3.x)
- pytest
- asyncio

###### Functional details:
1. Write a service which 2 times a day parses the rss showing movies added that day: https://yourbittorrent.com/movies/rss.xml
2. Save it to a db of choice, mind duplicates.
3. For each movie fetch it?s current imdb rating and genres.
4. Generate suggestions for a movie to download for each ?profile? saved in database. A single profile consists of:
    - minimal imdb rating
    - whitelist of genres (if at least one matches, it matches)
    - blacklist of genres (if at least one matches, it doesn?t match)
    - profile_id
5. Expose json API showing:
    - GET to list the suggestions for profile_id sorted with newest on top
    - POST call to dismiss a suggestion (mark it dismissed)
    - POST call to say a suggestion was a good one (mark it as good)
