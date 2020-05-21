from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, SelectField
from wtforms.validators import DataRequired


class ActorForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    gender = SelectField('gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    image_link = StringField('image_link')


class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    release_date = DateTimeField('release_date', validators=[DataRequired()])
    image_link = StringField('image_link')
