import base64
import requests
import pytz
from datetime import datetime, timedelta
from flask import session
from config import Config

client_id = Config.CLIENT_ID
client_secret = Config.CLIENT_SECRET
grant_type = {"grant_type": "client_credentials"}


class GuestAuth:
    TOKEN_URL = token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, grant_type):
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type

    def base64_encode(self, client_credentials):
        return base64.b64encode(client_credentials.encode())

    def authorize(self):
        token_headers = self.get_token_headers()

        post_response = requests.post(
            self.TOKEN_URL, headers=token_headers, data=self.grant_type
        )

        if post_response.status_code == 200:
            response_json = post_response.json()
            access_duration = response_json["expires_in"]
            expires_in = datetime.now() + timedelta(seconds=access_duration)
            session["expires_in"] = pytz.utc.localize(expires_in)

            access_token = response_json["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}

            session["access_token"] = access_token
            session["headers"] = headers

            return response_json

    def get_token_headers(self):
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = self.base64_encode(client_creds)

        return {
            "Authorization": f"Basic {client_creds_b64.decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_api_access_headers(self):
        expires = session["expires_in"]
        now = datetime.now()

        if expires < pytz.utc.localize(now):
            self.authorize()
            return self.get_api_access_headers()
        access_token = session["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        return headers


guest_auth = GuestAuth(client_id, client_secret, grant_type)
