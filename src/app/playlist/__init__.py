from flask import Blueprint

bp = Blueprint("playlist", __name__)

from app.playlist import routes
