from flask import redirect, render_template, request, Blueprint
from ybsuggestions.models import Profile, Movie, Genre, ProfileSuggestion
from ybsuggestions.forms import ProfileForm
from ybsuggestions import db


def get_defaults():
    if 'profile_id' in request.cookies:
        profile_id = int(request.cookies.get('profile_id'))
        current_profile = Profile.query.get(profile_id)
    else:
        current_profile = Profile.query.order_by(Profile.id.asc()).first()

    if not current_profile:
        current_profile = Profile(name='Default Profile', min_rating=0.0)
        db.session.add(current_profile)
        db.session.commit()
        db.session.flush()

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

    if context['current_profile'].blacklist:
        movies = Movie.query.filter(
            ~Movie.genres.any(
                Genre.id.in_(
                    [g.id for g in context['current_profile'].blacklist])),
            Movie.rating >= context['current_profile'].min_rating
        ).order_by(Movie.date.desc())
    else:
        movies = Movie.query.filter(
            Movie.rating >= context['current_profile'].min_rating
        ).order_by(Movie.date.desc())

    context.update({
        'movies': movies,
        'title': 'Home',
        'dismissed_movies': [s.movie_id for s in context['current_profile'].rated_suggestions if not s.was_liked],
        'liked_movies': [s.movie_id for s in context['current_profile'].rated_suggestions if s.was_liked]
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

        dismissed_suggestions = [s for s in profile.rated_suggestions if not s.was_liked]

        dismissed = []
        if dismissed_suggestions:
            for suggestion in dismissed_suggestions:
                dismissed.append((suggestion.id, Movie.query.get(suggestion.movie_id).name))

        context.update({
            'path': path,
            'form': form,
            'action': action,
            'dismissed': dismissed
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


@application_blueprint.route('/profile_suggestion/<int:profile_id>/<operation>/<int:ps_id>', methods=['GET'])
def profile_suggestion(profile_id='', ps_id='', operation=''):
    path = '/profile/%d' % profile_id

    if operation == 'delete':
        ps = ProfileSuggestion.query.get(ps_id)

        if ps:
            db.session.delete(ps)
            db.session.commit()

    return redirect(path)