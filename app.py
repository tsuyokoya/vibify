"""Vibify application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
import os
import re

app = Flask(__name__)


uri = os.environ.get("DATABASE_URL", "postgresql:///vibify")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Specify the database
app.config["SQLALCHEMY_DATABASE_URI"] = uri

# Default is True, turn off to prevent overhead
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Prints all SQL statements to terminal
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "as89hw8h2fisdfh903")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def show_home_page():
    """Renders home page"""

    return render_template("base.html")
