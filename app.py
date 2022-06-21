"""Vibify application."""

import logging
from flask import Flask, render_template, redirect, request, session, g, flash, Markup
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Playlist
from forms import CreatePlaylistForm
from spotify import spotify
from authentication import auth
from guest_authentication import guest_auth
from decimal import Decimal

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

CURR_USER_KEY = "curr_user"

debug = DebugToolbarExtension(app)
migrate = Migrate(app, db, compare_type=True)
connect_db(app)
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s : %(message)s",
)

##############################################################################
# Homepage


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def show_home_page():
    """Renders home page / Creates playlist"""
    form = CreatePlaylistForm()

    if form.validate_on_submit():
        vibe = round(form.vibe.data, 2)
        title = form.title.data

        if not title:
            title = f"my-playlist-vibe-{vibe}"

        session["title"] = title

        # Create playlist for guest user
        if g.user is None:
            guest_auth.authorize()
            spotify.create_user_playlist(vibe)
            return redirect(f"/playlists/{title}")

        # Create playlist for logged in user
        user_id = g.user.id
        playlist = Playlist.create(title, user_id)
        session["playlist_id"] = playlist.id
        spotify.create_user_playlist(vibe)

        return redirect(f"/playlists/{title}")

    return render_template("base.html", form=form)


##############################################################################
# User login/logout


@app.before_request
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


@app.route("/logout")
def logout_user():
    do_logout()
    session.clear()
    flash("Logged out", "danger")
    return redirect("/")


##############################################################################
# User Spotify authorization


@app.route("/authorize")
def register_with_spotify():
    """Authorizes use of user Spotify account data"""
    authorize_url = auth.get_authorization_url()
    app.logger.info(authorize_url)
    return redirect(authorize_url)


@app.route("/callback")
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


##############################################################################
# Playlist page


@app.route("/playlists", methods=["GET"])
def show_playlists_page():
    user_id = g.user.spotify_id
    playlists = spotify.get_user_playlists(user_id)

    if playlists:
        playlists_data = playlists[0]
        playlists_url = playlists[1]
        return render_template(
            "playlists.html", playlists_data=playlists_data, playlists_url=playlists_url
        )
    return render_template("playlists.html")


@app.route("/playlists", methods=["POST"])
def delete_playlist():
    playlist_id = request.form.get("playlist_to_delete")
    spotify.unfollow_playlist(playlist_id)
    flash("Deleted playlist", "danger")
    return redirect("/playlists")


@app.route("/playlists/<title>", methods=["GET", "POST"])
def show_generated_playlist(title):
    if request.method == "POST" and g.user is not None:
        user_id = g.user.spotify_id
        playlist_info = spotify.create_empty_spotify_playlist(user_id)
        playlist_id = playlist_info["id"]
        playlist_url = playlist_info["external_urls"]["spotify"]

        uris = [track["uri"] for track in session["playlist"]]

        spotify.populate_playlist(playlist_id, uris)
        flash(
            Markup(
                f"Successfully added playlist <a href='{playlist_url}' target='_blank' class='text-deepPurple underline'>HERE</a>"
            ),
            "success",
        )

        return redirect("/playlists")
    vibe = 0.00

    if title == "preset-neutral":
        vibe = 0.50
    elif title == "preset-happy":
        vibe = 1.00

    session["title"] = f"{title}"
    # Create preset playlist for guest user
    if g.user is None:
        guest_auth.authorize()
        spotify.create_user_playlist(Decimal(vibe))
        return render_template("playlist.html")

    # Create preset playlist for logged in user
    user_id = g.user.id
    playlist = Playlist.create(session["title"], user_id)
    session["playlist_id"] = playlist.id
    spotify.create_user_playlist(Decimal(vibe))

    return render_template("playlist.html")
