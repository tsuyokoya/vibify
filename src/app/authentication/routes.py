from flask import (
    current_app,
    flash,
    g,
    redirect,
    request,
    session,
)

from .spotify import spotify
from .authentication import auth

from app.authentication import bp
from app.models import User


CURR_USER_KEY = "curr_user"

#
# User login/logout
#


@bp.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@bp.route("/logout")
def logout_user():
    do_logout()
    session.clear()
    flash("Logged out", "danger")
    return redirect("/")


#
# User Spotify authorization
#


@bp.route("/authorize")
def register_with_spotify():
    """Authorizes use of user Spotify account data"""
    authorize_url = auth.get_authorization_url()
    current_app.logger.info(authorize_url)
    return redirect(authorize_url)


@bp.route("/callback")
def callback():
    """Exchanges the authorization code for an Access Token to complete spotify auth process"""
    # request.args returns a code and the state
    code = request.args.get("code")
    state = request.args.get("state")

    if state != session["state_key"]:
        return False
    is_authorized = auth.authorize_user(code)
    if is_authorized:
        user_data = spotify.get_user_spotify_data()
        is_registered = User.query.filter_by(email=user_data["email"]).first()

        if not is_registered:
            user = User.register(
                user_data["id"], user_data["display_name"], user_data["email"]
            )
            do_login(user)
        else:
            do_login(is_registered)
        flash("Successfully logged in", "success")
        return redirect("/")
