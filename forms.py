from flask_wtf import FlaskForm
from wtforms import StringField, IntegerRangeField, EmailField, PasswordField
from wtforms.validators import InputRequired, Email, NumberRange, Length


class CreatePlaylistForm(FlaskForm):
    """Form for creating a new playlist"""

    title = StringField("Playlist Title", validators=[InputRequired()])
    vibe = IntegerRangeField(validators=[NumberRange(min=0, max=10)])


class LoginForm(FlaskForm):
    """Form for user login"""

    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    """Form for user registration"""

    first_name = StringField("First Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8)])
