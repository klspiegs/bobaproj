from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("search for boba places!")

class FriendSearchForm(FlaskForm):
    friend_search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("search for friends!")


class BobaReview(FlaskForm):
    text = TextAreaField(
        "review", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("review!")


class RegistrationForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("email", validators=[InputRequired(), Email()])
    password = PasswordField("password", validators=[InputRequired()])
    confirm_password = PasswordField("confirm password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("sign up!")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("username is taken :(")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("email is taken :(")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    submit = SubmitField("login")


class UpdateUsernameForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("update your username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("that username is already taken D:")
