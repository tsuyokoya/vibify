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


@bp.route("/home", methods=["GET", "POST"])
@bp.route("/", methods=["GET", "POST"])
def show_home_page():
    """Renders home page / Creates playlist"""
    form = CreatePlaylistForm()

    if form.validate_on_submit():
        vibe = round(form.vibe.data, 2)
        title = form.title.data

        if not title:
            title = f"my-playlist-{datetime.now().date()}"

        session["title"] = title

        # Create playlist for guest user
        if g.user is None:
            guest_auth.authorize()
            spotify.create_user_playlist(vibe)
            return redirect(f"/playlist/{title}")

        # Create playlist for logged in user
        spotify.create_user_playlist(vibe)

        return redirect(f"/playlist/{title}")

    return render_template("base.html", form=form)
