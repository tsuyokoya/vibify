import requests

BASE_URL = "https://api.spotify.com/v1"


def get_user_spotify_data(json):
    headers = {"Authorization": f"Bearer {json['access_token']}"}
    lookup_url = BASE_URL + "/me"
    user_data = requests.get(lookup_url, headers=headers)
    return user_data.json()
