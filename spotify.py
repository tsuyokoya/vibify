import base64
from os import access
import random
import string
import requests
import pytz
from urllib.parse import urlencode
from datetime import datetime, timedelta
from flask import session


class SpotifyAPI:
    TOKEN_URL = token_url = "https://accounts.spotify.com/api/token"
    AUTH_BASE_URL = "https://accounts.spotify.com/en/authorize?"
    ENDPOINT_BASE_URL = "https://api.spotify.com/v1"

    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

    def create_state_key(self):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for i in range(15))

    def base64_encode(self, client_credentials):
        return base64.b64encode(client_credentials.encode())

    def get_authorization_url(self):
        """Returns authorization redirect URL"""
        state_key = self.create_state_key()

        session["state_key"] = state_key

        query = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": state_key,
        }
        authorize_url = self.AUTH_BASE_URL + urlencode(query)
        return authorize_url

    def authorize_user(self, code):
        token_headers = self.get_token_headers()
        token_data = self.get_token_data(code)
        post_response = requests.post(
            self.TOKEN_URL, headers=token_headers, data=token_data
        )
        if post_response.status_code == 200:
            response_json = post_response.json()
            access_duration = response_json["expires_in"]
            expires_in = datetime.now() + timedelta(seconds=access_duration)
            session["expires_in"] = pytz.utc.localize(expires_in)

            access_token = response_json["access_token"]
            refresh_token = response_json["refresh_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            session["access_token"] = access_token
            session["refresh_token"] = refresh_token
            session["headers"] = headers

            return True

    def get_token_headers(self):
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = self.base64_encode(client_creds)
        return {
            "Authorization": f"Basic {client_creds_b64.decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_token_data(self, code):
        return {
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

    def get_refreshed_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
        }
        headers = self.get_token_headers()
        post_response = requests.post(self.TOKEN_URL, data=data, headers=headers).json()

        access_token = post_response["access_token"]
        access_duration = post_response["expires_in"]
        expires_in = datetime.now() + timedelta(seconds=access_duration)

        session["expires_in"] = pytz.utc.localize(expires_in)
        session["access_token"] = access_token
        return post_response

    def get_api_access_headers(self):
        expires = session["expires_in"]
        now = datetime.now()

        if expires < pytz.utc.localize(now):
            self.get_refreshed_token()
            return self.get_api_access_headers()
        access_token = session["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        return headers

    def get_user_spotify_data(self):
        lookup_url = self.ENDPOINT_BASE_URL + "/me"
        headers = session["headers"]

        user_data = requests.get(lookup_url, headers=headers)
        return user_data.json()

    def create_user_playlist(self):
        # featured_playlists_ids = self.get_featured_playlists()
        new_albums_ids = self.get_new_albums()
        track_ids = self.get_albums_tracks(new_albums_ids)
        raise

    def get_new_albums(self):
        new_albums_ids = []
        endpoint = self.ENDPOINT_BASE_URL + "/browse/new-releases"
        headers = self.get_api_access_headers()

        new_albums_data = requests.get(endpoint, headers=headers).json()
        new_albums_items = new_albums_data["albums"]["items"]

        new_albums_ids = [album["id"] for album in new_albums_items]

        return new_albums_ids

    def get_albums_tracks(self, ids):
        string_ids = ",".join(ids)
        query = {"ids": string_ids}
        endpoint = self.ENDPOINT_BASE_URL + f"/albums?{urlencode(query)}"
        headers = self.get_api_access_headers()

        albums_data = requests.get(endpoint, headers=headers).json()
        albums_list = albums_data["albums"]

        tracks_ids = [
            [track["id"] for track in album["tracks"]["items"]] for album in albums_list
        ]

        return tracks_ids
