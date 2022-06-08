"""Vibify application."""

import base64
import requests
import urllib
import logging
from flask import Flask, render_template, redirect, request, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Playlist, Song, Playlist_Song
from forms import CreatePlaylistForm, LoginForm, RegistrationForm
from spotify import SpotifyAPI

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

debug = DebugToolbarExtension(app)
migrate = Migrate(app, db)
connect_db(app)
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s : %(message)s",
)

client_id = app.config["CLIENT_ID"]
client_secret = app.config["CLIENT_SECRET"]
redirect_uri = app.config["REDIRECT_URI"]
scope = app.config["SCOPE"]
spotify = SpotifyAPI(client_id, client_secret, redirect_uri, scope)


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def show_home_page():
    """Renders home page / Creates playlist"""
    form = CreatePlaylistForm()

    if form.validate_on_submit():
        user_id = g.user.id or "guest"
        Playlist.create(form.title.data, form.vibe.data, user_id)
        playlist = spotify.create_user_playlist()
        app.logger.info(playlist)

        flash("Successfully created playlist", "success")
        return redirect("/playlists")

    return render_template("base.html", form=form)


##############################################################################
# User login/logout/registration

CURR_USER_KEY = "curr_user"


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/login", methods=["GET", "POST"])
def show_login_page():
    """Renders login page / logs in user"""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data, form.password.data)

        if user:
            do_login(user)
            flash("Successfully logged in", "success")
            return redirect("/")

        flash("Invalid email / password", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_user():
    do_logout()
    flash("Logged out", "danger")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def show_register_page():
    """Renders registration page / registers new user"""
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.register(form.first_name.data, form.email.data, form.password.data)

        if user:
            do_login(user)
            flash("Successfully logged in", "success")
            return redirect("/")

        flash("Invalid email / password", "danger")
    return render_template("register.html", form=form)


@app.route("/authorize")
def register_with_spotify():
    """Authorizes use of user Spotify account data"""
    authorize_url = spotify.get_authorization_url()
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
    is_authorized = spotify.authorize_user(code)
    if is_authorized:
        user_data = spotify.get_user_spotify_data()
        user = User.register(user_data["display_name"], user_data["email"], "password")
        do_login(user)
        return redirect("/")


@app.route("/playlists", methods=["GET", "POST"])
def show_playlists_page():
    return render_template("playlists.html")
