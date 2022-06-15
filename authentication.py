import base64
import random
import string
import requests
import pytz
from urllib.parse import urlencode
from datetime import datetime, timedelta
from flask import session
from config import Config

client_id = Config.CLIENT_ID
client_secret = Config.CLIENT_SECRET
redirect_uri = Config.REDIRECT_URI
scope = Config.SCOPE


class Authentication:
    TOKEN_URL = token_url = "https://accounts.spotify.com/api/token"
    AUTH_BASE_URL = "https://accounts.spotify.com/en/authorize?"

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


auth = Authentication(client_id, client_secret, redirect_uri, scope)
