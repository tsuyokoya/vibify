from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    DecimalRangeField,
)
from wtforms.validators import InputRequired, Email, NumberRange, Length


class CreatePlaylistForm(FlaskForm):
    """Form for creating a new playlist"""

    title = StringField(
        "Playlist Title",
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter playlist title"},
    )
    vibe = DecimalRangeField(validators=[NumberRange(min=0, max=10)])


class LoginForm(FlaskForm):
    """Form for user login"""

    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    """Form for user registration"""

    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(min=4, max=20)]
    )
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
