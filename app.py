"""Vibify application."""

import base64
import requests
import spotify
import urllib
from flask import Flask, render_template, redirect, request, session, g, make_response
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
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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


@app.route("/authorize")
def register_with_spotify():
    """Authorizes use of user Spotify account data"""
    client_id = app.config["CLIENT_ID"]
    redirect_uri = app.config["REDIRECT_URI"]
    scope = app.config["SCOPE"]
    # print(client_id, redirect_uri, scope)
    # need to update state_key
    # state_key = "1234567890qwert"
    # session["state_key"] = state_key

    # authorize_base_url = "https://accounts.spotify.com/en/authorize?"
    # query = {
    #     "response_type": "code",
    #     "client_id": client_id,
    #     "redirect_uri": redirect_uri,
    #     "scope": scope,
    #     "state": state_key,
    # }
    # print(authorize_base_url + urllib.parse.urlencode(query))
    # authorize_url = authorize_base_url + urllib.parse.urlencode(query)
    authorize_url = spotify.authorize_user(client_id, redirect_uri, scope)
    print("************", authorize_url)

    return redirect(authorize_url)

    # make response
    # use to add more headers / edit the response
    # takes input and uses it in body of response -> resulting body allows you to customize response
    # basically what flask does internally
    # my_resp.headers[''] = ''


@app.route("/callback")
def callback():
    print("******************", request.args)
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
        token_url = "https://accounts.spotify.com/api/token"

        # token_headers = {
        #     "Authorization": f"Basic {client_creds_b64.decode()}",
        #     "Accept": "application/json",
        #     "Content-Type": "application/x-www-form-urlencoded",
        # }
        # token_data = {
        #     "code": code,
        #     "redirect_uri": redirect_uri,
        #     "grant_type": "authorization_code",
        # }
        token_headers = spotify.get_token_headers(client_creds)
        token_data = spotify.get_token_data(code, redirect_uri)
        post_response = requests.post(token_url, headers=token_headers, data=token_data)
        print("THIS IS THE POST RESPONSE", post_response.json())

        # 200 code indicates access token was properly granted
        if post_response.status_code == 200:
            json = post_response.json()
            print("THIS IS THE JSON", json)
            # return json["access_token"], json["refresh_token"], json["expires_in"]
            return redirect("/")
        # else:
        #     return redirect("/404")
