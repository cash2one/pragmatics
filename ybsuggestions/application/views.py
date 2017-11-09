from flask import flash, url_for, redirect, render_template, request, Blueprint
import requests
import json
from ybsuggestions.models import Profile, Movie, Genre
from ybsuggestions.forms import ProfileForm, MovieForm
from ybsuggestions import db


def get_defaults():
    if 'profile_id' in request.cookies:
        profile_id = int(request.cookies.get('profile_id'))
        current_profile = Profile.query.get(profile_id)
    else:
        current_profile = Profile.query.order_by(Profile.id.asc()).first()

    profiles = Profile.query.all()
    if not profiles:
        profiles = None

    defaults = {
        'profiles': profiles,
        'current_profile': current_profile
    }

    return defaults


application_blueprint = Blueprint('application', __name__, template_folder='templates')


@application_blueprint.route('/')
@application_blueprint.route('/index')
def index():
    context = get_defaults()

    movies = Movie.query.filter(
        ~Movie.genres.any(
            Genre.id.in_(
                [g.id for g in context['current_profile'].blacklist])),
        Movie.rating >= context['current_profile'].min_rating
    ).order_by(Movie.date.desc())

    context.update({
        'movies': movies,
        'title': 'Home'
    })

    return render_template("index.html", **context)


@application_blueprint.route('/profile/', methods=['GET', 'POST'])
@application_blueprint.route('/profile/<int:profile_id>/', methods=['GET', 'POST'])
@application_blueprint.route('/profile/<operation>/', methods=['GET'])
@application_blueprint.route('/profile/<operation>/<int:profile_id>', methods=['GET'])
def profile(profile_id='', operation=''):
    if request.method == 'POST':
        return post_profile(profile_id=profile_id)
    else:
        return get_profile(profile_id=profile_id, operation=operation)


def get_profile(profile_id='', operation=''):
    context = get_defaults()
    path = '/profile/'
    form = ProfileForm()

    if operation == 'new':

        context.update({
            'path': path,
            'form': form,
            'action': path
        })

        return render_template("profile_detail.html", **context)

    if operation == 'delete':
        obj = Profile.query.get(profile_id)
        db.session.delete(obj)
        db.session.commit()
        return redirect(path)

    if profile_id:
        profile = Profile.query.get(profile_id)

        form = ProfileForm(obj=profile)

        action = request.path

        context.update({
            'path': path,
            'form': form,
            'action': action
        })

        return render_template("profile_detail.html", **context)

    profiles = Profile.query.all()

    context.update({
        'path': path,
        'obj': profiles,
    })

    return render_template("profile_list.html", **context)


def post_profile(profile_id=''):
    path = '/profile/'

    if profile_id:
        profile = Profile.query.get(profile_id)
    else:
        profile = Profile()

    form = ProfileForm(request.form)
    form.populate_obj(profile)

    db.session.add(profile)
    db.session.commit()

    return redirect(path)


# @application_blueprint.route('/movie/', methods=['GET', 'POST'])
# @application_blueprint.route('/movie/<int:movie_id>/', methods=['GET', 'POST'])
# def movie(movie_id='', operation=''):
#     if request.method == 'POST':
#         return post_movie(movie_id=movie_id)
#     else:
#         return get_movie(movie_id=movie_id, operation=operation)
#
#
# def get_movie(movie_id='', operation=''):
#
#     path = '/movie/'
#     form = MovieForm()
#
#     if operation == 'new':
#         return render_template("object_detail.html", path=path, form=form, action=path)
#
#     if operation == 'delete':
#         obj = Movie.query.get(movie_id)
#         db.session.delete(obj)
#         db.session.commit()
#         return redirect(path)
#
#     if movie_id:
#         movie = Movie.query.get(movie_id)
#
#         form = MovieForm(obj=movie)
#
#         action = request.path
#         return render_template("object_detail.html", path=path, form=form, action=action)
#
#     movies = Movie.query.all()
#     return render_template("movie_list.html", path=path, obj=movies)
#
#
# def post_movie(movie_id=''):
#     path = '/movie/'
#
#     if movie_id:
#         movie = Movie.query.get(movie_id)
#     else:
#         movie = Movie()
#
#     form = MovieForm(request.form)
#     form.populate_obj(movie)
#
#     db.session.add(movie)
#     db.session.commit()
#
#     return redirect(path)