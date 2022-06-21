"""Vibify routes tests."""
import sys

sys.path.append("../")
from unittest import TestCase
from app import app


class RoutesTestCase(TestCase):
    """Test routes."""

    def setUp(self):
        """Create test client"""
        self.client = app.test_client()

    def test_home_page(self):
        """Does home page render?"""

        with self.client as c:
            res = c.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Generate Spotify playlists based on your vibe", html)
            self.assertIn("Sign In", html)
