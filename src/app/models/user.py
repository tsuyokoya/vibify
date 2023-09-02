import uuid

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


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
