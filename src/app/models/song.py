from app.extensions import db


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
