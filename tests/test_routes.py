"""Vibify routes tests."""

from unittest import TestCase

# from models import db, User, Playlist, Song, Playlist_Song
# import os
# os.environ["DATABASE_URL"] = "postgresql:///vibify"

from app import app

# db.create_all()


class RoutesTestCase(TestCase):
    """Test routes."""

    def test_home_page(self):
        """Does home page render?"""

        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Generate Spotify playlists based on your vibe.", html)

    def test_login_page(self):
        """Does login page render?"""

        with app.test_client() as client:
            res = client.get("/login")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("New to Vibify? Sign Up", html)
