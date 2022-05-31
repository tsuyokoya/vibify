import base64
import random
import string
import urllib
from flask import session


class SpotifyAPI:
    def create_state_key(self):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for i in range(15))

    def base64_encode(self, client_credentials):
        return base64.b64encode(client_credentials.encode())

    def authorize_user(self, client_id, redirect_uri, scope):
        """Authorizes the use of user Spotify account data"""
        state_key = self.create_state_key()

        session["state_key"] = state_key

        authorize_base_url = "https://accounts.spotify.com/en/authorize?"
        query = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state_key,
        }
        authorize_url = authorize_base_url + urllib.parse.urlencode(query)

        return authorize_url

    def get_token_headers(self, client_creds):
        client_creds_b64 = self.base64_encode(client_creds)
        return {
            "Authorization": f"Basic {client_creds_b64.decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_token_data(self, code, redirect_uri):
        return {
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

    def get_refreshed_token(self, refresh_token):
        return {"grant_type": "refresh_token", "refresh_token": refresh_token}
