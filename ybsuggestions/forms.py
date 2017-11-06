from ybsuggestions.models import Genre
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    """
    Form for users to create new account
    """
    genres = Genre.query.all()
    genres_choices = []
    for genre in genres:
        genres_choices.append((genre.id, genre.name))

    name = StringField(validators=[DataRequired()])
    whitelist = SelectMultipleField(choices=genres_choices)
    blacklist = SelectMultipleField(choices=genres_choices)
