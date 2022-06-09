from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalRangeField,
)
from wtforms.validators import InputRequired, NumberRange


class CreatePlaylistForm(FlaskForm):
    """Form for creating a new playlist"""

    title = StringField(
        "Playlist Title",
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter playlist title"},
    )
    vibe = DecimalRangeField(validators=[NumberRange(min=0, max=10)])
