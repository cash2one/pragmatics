## Task Summary:

#### Configuration:
- Repository: https://github.com/harzo/pragmatics
- Docker settings in Dockerfile and docker-compose.yml
- Possible AWS deploy: http://18.216.240.105/

#### Requirements:
- db: used PostgreSQL db on private server
- imdbpy: used in 'ybsuggestions/crawler' module (imdbpy_p2script.py)
- asyncio: used in 'ybsuggestions/crawler' module (jobs.py), main loop created in 'ybsuggestions' init
- pytest: test stored in 'tests' directory

#### Functionalities:

###### RSS parsing:
- YBParser in 'ybsuggestions/crawler' module.
- For parsing xml used 'feedparser' library
- For parsing torrents names used 'ptn' library
- Because of often YourBitTorrent server problems and Cloudflare CAPTCHA screen, on deployment used similar feed from https://rarbg.to/rssdd.php?category=movies

###### Fetching IMDb rating and genres:
- Job 'job_check_new_movies' in 'ybsuggestions/crawler/jobs.py' create async task for each movie.
- Async 'call_imdbpy' in 'ybsuggestions/crawler/jobs.py' runs Python2 script for fetching imdb rating.
- Python2 'imdbpy_p2script.py' in 'ybsuggestions/crawler' use 'imdbpy'.

###### Calling 2 times a day:
- Side Thread created in 'ybsuggestions' init.
- Job 'job_check_new_movies' added to schedule executing sctipt each 12 hours.

###### Objects CRUD:
- Used Flask sql-alchemy to managing objects (Movie, Profile, Genre)
- For Movie created special data access class - MovieDAO in 'ybsuggestions/crawler/moviedao.py'

###### Apis:
- Created as Flask blueprint in 'ybsuggestions/application/apis.py'

***

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
