import base64
import random
import string
import urllib
from flask import session


def create_state_key(num):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(num))


def base64_encode(client_credentials):
    return base64.b64encode(client_credentials.encode())


def authorize_user(client_id, redirect_uri, scope):
    """Authorizes the use of user Spotify account data"""
    state_key = create_state_key(15)

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


def get_token_headers(client_creds):

    client_creds_b64 = base64_encode(client_creds)
    return {
        "Authorization": f"Basic {client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }


def get_token_data(code, redirect_uri):
    return {
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }


def get_refreshed_token(refresh_token):
    return {"grant_type": "refresh_token", "refresh_token": refresh_token}
