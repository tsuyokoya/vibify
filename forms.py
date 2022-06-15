from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DecimalRangeField,
)
from wtforms.validators import NumberRange, Length


class CreatePlaylistForm(FlaskForm):
    """Form for creating a new playlist"""

    title = StringField(
        "Playlist Title",
        render_kw={"placeholder": "Enter playlist title"},
        validators=[Length(max=20)],
    )
    vibe = DecimalRangeField(validators=[NumberRange(min=0, max=1)])
