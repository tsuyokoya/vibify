from multiprocessing import AuthenticationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import UUID
import uuid

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Vibify."""

# - users
#   - id: TEXT, PK (uuid)
#   - first_name: VARCHAR(25)
#   - email: VARCHAR(50), unique
#   - password: TEXT (hashed)

# User model
class User(db.Model):
    """Creates user model"""

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, first_name, email, password):
        """Register user. Password is hashed. Adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            first_name=first_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user

    playlists = db.relationship(
        "Playlist",
        backref="user",
    )

    @classmethod
    def authenticate(cls, email, password):
        """Authenticate user login information"""

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


# - playlists
#   - id: TEXT, PK (uuid)
#   - name: VARCHAR(25)
#   - description: VARCHAR(100)
#   - user_id: TEXT, FK

# Playlist model
class Playlist(db.Model):
    """Creates playlist model"""

    __tablename__ = "playlists"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(100))
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="cascade")
    )

    songs = db.relationship(
        "Song",
        secondary="playlists_songs",
        backref="playlists",
    )

    @classmethod
    def create(cls, name, description, user_id):
        playlist = Playlist(name=name, description=description, user_id=user_id)
        db.session.add(playlist)
        db.session.commit()
        return playlist


# - songs
#   - id: TEXT, PK (uuid)
#   - title: VARCHAR(50)
#   - artist: VARCHAR(50)
#   - album: VARCHAR(50)
#   - artwork: TEXT
#   - preview_url: TEXT

# Song model
class Song(db.Model):
    """Creates song model"""

    __tablename__ = "songs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    album = db.Column(db.String(50))
    artwork = db.Column(db.Text)
    preview_url = db.Column(db.Text)


# - playlists_songs
#   - playlist_id: TEXT, FK
#   - song_id: TEXT, FK

# Playlist_Song model
class Playlist_Song(db.Model):
    """Connection of a playlist <-> song."""

    __tablename__ = "playlists_songs"

    playlist_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("playlists.id", ondelete="cascade"),
        primary_key=True,
    )

    song_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("songs.id", ondelete="cascade"),
        primary_key=True,
    )
