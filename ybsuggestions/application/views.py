from flask import flash, redirect, render_template, request, Blueprint
from ybsuggestions.models import Profile, Movie
from ybsuggestions.forms import ProfileForm, MovieForm
from ybsuggestions import db


def render_with_defaults(template, **kwargs):
    profile = Profile.query.order_by(Profile.id.asc()).first()

    return render_template(template, **kwargs, profile=profile)


application_blueprint = Blueprint('application', __name__, template_folder='templates')


@application_blueprint.route('/')
@application_blueprint.route('/index')
def index():
    movies = Movie.query.order_by(Movie.date.desc()).all()

    return render_with_defaults("index.html", movies=movies, title='Home')


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

    path = '/profile/'
    form = ProfileForm()

    if operation == 'new':
        return render_template("object_detail.html", path=path, form=form, action=path)

    if operation == 'delete':
        obj = Profile.query.get(profile_id)
        db.session.delete(obj)
        db.session.commit()
        return redirect(path)

    if profile_id:
        profile = Profile.query.get(profile_id)

        form = ProfileForm(obj=profile)

        action = request.path
        return render_template("object_detail.html", path=path, form=form, action=action)

    profiles = Profile.query.all()
    return render_template("profile_list.html", path=path, obj=profiles)


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


@application_blueprint.route('/movie/', methods=['GET', 'POST'])
@application_blueprint.route('/movie/<int:movie_id>/', methods=['GET', 'POST'])
# @application_blueprint.route('/profile/<operation>/', methods=['GET'])
# @application_blueprint.route('/profile/<operation>/<int:movie_id>', methods=['GET'])
def movie(movie_id='', operation=''):
    if request.method == 'POST':
        return post_movie(movie_id=movie_id)
    else:
        return get_movie(movie_id=movie_id, operation=operation)
    
    
def get_movie(movie_id='', operation=''):

    path = '/movie/'
    form = MovieForm()

    if operation == 'new':
        return render_template("object_detail.html", path=path, form=form, action=path)

    if operation == 'delete':
        obj = Movie.query.get(movie_id)
        db.session.delete(obj)
        db.session.commit()
        return redirect(path)

    if movie_id:
        movie = Movie.query.get(movie_id)

        form = MovieForm(obj=movie)

        action = request.path
        return render_template("object_detail.html", path=path, form=form, action=action)

    movies = Movie.query.all()
    return render_template("movie_list.html", path=path, obj=movies)


def post_movie(movie_id=''):
    path = '/movie/'

    if movie_id:
        movie = Movie.query.get(movie_id)
    else:
        movie = Movie()

    form = MovieForm(request.form)
    form.populate_obj(movie)

    db.session.add(movie)
    db.session.commit()

    return redirect(path)