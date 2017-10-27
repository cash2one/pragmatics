from flask import render_template, Blueprint

application_blueprint = Blueprint('app', __name__, template_folder='templates')


@application_blueprint.route('/')
@application_blueprint.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("base.html",
                           title='Home',
                           user=user,
                           posts=posts)
