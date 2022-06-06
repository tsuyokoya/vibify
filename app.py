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
from helpers import get_user_spotify_data

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

token_url = "https://accounts.spotify.com/api/token"

spotify = SpotifyAPI()


@app.route("/home")
@app.route("/")
def show_home_page():
    """Renders home page"""
    form = CreatePlaylistForm()
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

        flash("Invalid email / password", "warning")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_user():
    do_logout()
    flash("Logged out", "warning")
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

        flash("Invalid email / password", "warning")
    return render_template("register.html", form=form)


@app.route("/authorize")
def register_with_spotify():
    """Authorizes use of user Spotify account data"""
    client_id = app.config["CLIENT_ID"]
    redirect_uri = app.config["REDIRECT_URI"]
    scope = app.config["SCOPE"]

    authorize_url = spotify.authorize_user(client_id, redirect_uri, scope)
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
    else:
        redirect_uri = app.config["REDIRECT_URI"]
        client_secret = app.config["CLIENT_SECRET"]
        client_id = app.config["CLIENT_ID"]
        client_creds = f"{client_id}:{client_secret}"

        token_headers = spotify.get_token_headers(client_creds)
        token_data = spotify.get_token_data(code, redirect_uri)
        post_response = requests.post(token_url, headers=token_headers, data=token_data)

        if post_response.status_code == 200:
            json = post_response.json()
            user_data = get_user_spotify_data(json)
            user = User.register(
                user_data["display_name"], user_data["email"], "password"
            )
            do_login(user)
            return redirect("/")


@app.route("/playlists")
def show_playlists_page():
    return render_template("playlists.html")
