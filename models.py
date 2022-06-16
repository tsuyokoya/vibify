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
    spotify_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def register(cls, spotify_id, name, email):
        """Register user. Password is hashed. Adds user to system."""

        user = User(
            spotify_id=spotify_id,
            name=name,
            email=email,
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
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="cascade")
    )

    songs = db.relationship(
        "Song",
        secondary="playlists_songs",
        backref="playlists",
    )

    @classmethod
    def create(cls, name, user_id):
        playlist = Playlist(name=name, user_id=user_id)
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

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    valence = db.Column(db.Numeric(3, 2))
    uri = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    album_name = db.Column(db.String)
    album_image_url = db.Column(db.String)

    @classmethod
    def create(cls, id, name, uri, artist, album_name, album_image_url):
        song = Song(
            id=id,
            name=name,
            uri=uri,
            artist=artist,
            album_name=album_name,
            album_image_url=album_image_url,
        )
        db.session.add(song)
        db.session.commit()
        return song


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
        db.String,
        db.ForeignKey("songs.id", ondelete="cascade"),
        primary_key=True,
    )

    @classmethod
    def create(cls, playlist_id, song_id):
        playlist_song = Playlist_Song(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        return playlist_song
