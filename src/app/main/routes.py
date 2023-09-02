from datetime import datetime
from flask import render_template, redirect, session, g

from app.authentication import guest_auth, spotify
from app.main import bp
from app.models import User

from ..forms import CreatePlaylistForm

CURR_USER_KEY = "curr_user"


# runs before all requests in all blueprints
@bp.before_app_request
def add_user_to_g():
    """If logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@bp.route("/", methods=["GET"])
def show_home_page():
    form = CreatePlaylistForm()

    return render_template("base.html", form=form)
