"""Vibify forms tests."""
import sys

sys.path.append("../")
from unittest import TestCase
from forms import CreatePlaylistForm
from app import app


class FormsTestCase(TestCase):
    """Test forms."""

    def test_playlist_form(self):
        """Does the playlist form handle correct inputs?"""

        with app.app_context():
            form = CreatePlaylistForm()

            # valid inputs, should be True
            form.vibe.data = 0.5
            form.title.data = "my-playlist"
            self.assertTrue(form.validate())

            # invalid input (vibe > 1), should be False
            form.vibe.data = 1.5
            form.title.data = "my-playlist"
            self.assertFalse(form.validate())
