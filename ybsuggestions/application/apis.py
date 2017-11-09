import json
from flask import jsonify, Blueprint, request
from ybsuggestions import db
from ybsuggestions.models import Movie, Profile, Genre, ProfileSuggestion

apis_blueprint = Blueprint('apis', __name__, template_folder='templates')


@apis_blueprint.route('/get_suggestions/<int:profile_id>', methods=['GET'])
def get_suggestions(profile_id):
    profile = Profile.query.get(profile_id)

    if profile is None:
        movies = Movie.query.all()
    else:
        movies = Movie.query.filter(
            ~Movie.genres.any(
                Genre.id.in_(
                    [g.id for g in profile.blacklist])),
            Movie.rating >= profile.min_rating
        ).order_by(Movie.date.desc())

    json_movies = []
    for movie in movies:
        json_movies.append(movie.to_json())

    return jsonify({'movies': json_movies})


def create_profile_suggestion(profile_id, movie_id, was_liked):

    profile_suggestion = ProfileSuggestion()

    profile_suggestion.profile_id = profile_id
    profile_suggestion.movie_id = movie_id
    profile_suggestion.was_liked = was_liked

    db.session.add(profile_suggestion)
    db.session.commit()

    return profile_suggestion.id


def handle_profile_suggestion_api(json_data):

    try:
        profile_id = json_data['profile_id']
        movie_id = json_data['movie_id']
        was_liked = json_data['was_liked']
    except KeyError:
        return jsonify({'status': 'failure', 'message': 'KeyError. Provided data are corrupted.'})

    id = create_profile_suggestion(profile_id, movie_id, was_liked)

    if id:
        return jsonify({'status': 'success', 'id': id})
    else:
        return jsonify({'status': 'failure', 'message': 'DbError. Please try again.'})


@apis_blueprint.route('/post_dismiss_suggestion', methods=['POST'])
def post_dismiss_suggestion():
    request.get_data()
    data = request.data
    data_dict = json.loads(data)
    data_dict['was_liked'] = False

    return handle_profile_suggestion_api(data_dict)


@apis_blueprint.route('/post_good_suggestion', methods=['POST'])
def post_good_suggestion():
    request.get_data()
    data = request.data
    data_dict = json.loads(data)
    data_dict['was_liked'] = True

    return handle_profile_suggestion_api(data_dict)