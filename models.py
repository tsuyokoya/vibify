from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Vibify."""

# - users
#   - id: UUID, PK
#   - spotify_id: String
#   - name: String
#   - email: String

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
        """Registers user and adds user to database."""

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


# - songs
#   - id: String, PK
#   - name: String
#   - valence: Decimal
#   - uri: String
#   - artist: String
#   - album_name: String
#   - album_image_url: String

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
