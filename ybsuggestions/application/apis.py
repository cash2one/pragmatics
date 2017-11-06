from flask import jsonify
from ybsuggestions import app
from ybsuggestions.models import Movie, Profile, Genre


@app.route('/get_suggestions', methods=['GET'])
@app.route('/get_suggestions/<int:profile_id>', methods=['GET'])
def get_suggestions(profile_id=None):
    profile = None
    if profile_id is not None:
        profile = Profile.query.get(profile_id)

    if profile is None:
        movies = Movie.query.all()
    else:
        movies = Movie.guery.filter(Movie.genres.any(
                        Genre.id.in_(profile.whitelist),
                        ~Genre.id.in_(profile.blacklist)))

    json_movies = []
    for movie in movies:
        json_movies.append(movie.to_json())

    return jsonify({'movies': json_movies})