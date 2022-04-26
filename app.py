"""Vibify application."""

from flask import Flask, render_template, redirect, request, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from models import db, connect_db, User, Playlist, Song, Playlist_Song
from forms import CreatePlaylistForm, LoginForm, RegistrationForm

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

debug = DebugToolbarExtension(app)
migrate = Migrate(app, db)
connect_db(app)


@app.route("/")
def show_home_page():
    """Renders home page"""
    form = CreatePlaylistForm()
    return render_template("base.html", form=form)


@app.route("/login")
def show_login_page():
    """Renders login page"""
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register")
def show_register_page():
    """Renders registration page"""
    form = RegistrationForm()
    return render_template("register.html", form=form)


##############################################################################
# User login/logout

CURR_USER_KEY = "curr_user"


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
