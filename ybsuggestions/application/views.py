from flask import flash, redirect, url_for, render_template, request, Blueprint
from ybsuggestions.models import Profile, Genre
from ybsuggestions.forms import ProfileForm
from ybsuggestions import db

application_blueprint = Blueprint('app', __name__, template_folder='templates')


@application_blueprint.route('/')
@application_blueprint.route('/index')
def index():
    return render_template("index.html", title='Home')


@application_blueprint.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    form = ProfileForm()
    print('Step1')
    if form.validate_on_submit():
        print('Step2')
        whitelist = [g[0] for g in form.whitelist.data]
        blacklist = [g[0] for g in form.blacklist.data]

        print('Step3')
        profile = Profile(name=form.name.data,
                            whitelist=Genre.query.filter(Genre.id.in_(whitelist), ~Genre.id.in_(blacklist)),
                            first_name=Genre.query.filter(Genre.id.in_(blacklist), ~Genre.id.in_(whitelist)))

        # add employee to the database
        db.session.add(profile)
        db.session.commit()
        flash('Profile added successfully')

        return redirect(url_for('index'))

    return render_template('profile_add.html', title='Add profile', form=form)