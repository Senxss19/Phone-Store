from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField("Login", name='submit')


class SignupForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired()]
    )
    nickname = StringField(
        'Nickname',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField("Signup", name='submit')


class ProfileForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired()],
        render_kw={'disabled': True}
    )
    nickname = StringField(
        'Nickname',
        validators=[DataRequired()]
    )

    submit = SubmitField("Update Profile", name='submit')


class PasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
    )
    confirm = StringField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    submit = SubmitField("Update Password", name='submit')
