from ybsuggestions.models import Genre
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField


def genre_choices():
    return Genre.query.all()


class ProfileForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    whitelist = QuerySelectMultipleField('Whitelist', query_factory=genre_choices)
    blacklist = QuerySelectMultipleField('Blacklist', query_factory=genre_choices)


class MovieForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    rating = FloatField(default=0.0)
    genres = QuerySelectMultipleField('Whitelist', query_factory=genre_choices)
