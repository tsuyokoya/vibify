import requests
from urllib.parse import urlencode
from flask import session
from decimal import Decimal
from random import shuffle
from models import db, Song, Playlist_Song

from authentication import auth


class SpotifyAPI:
    ENDPOINT_BASE_URL = "https://api.spotify.com/v1"

    def get_user_spotify_data(self):
        lookup_url = self.ENDPOINT_BASE_URL + "/me"
        headers = session["headers"]

        user_data = requests.get(lookup_url, headers=headers)
        return user_data.json()

    def create_user_playlist(self, vibe, playlist_id):
        headers = auth.get_api_access_headers()

        new_albums_ids = self.get_new_albums(headers)
        track_ids = self.get_albums_tracks(headers, new_albums_ids)
        grouped_track_ids = self.group_track_ids(track_ids, 100)
        tracks_features = self.get_tracks_audio_features(headers, grouped_track_ids)
        playlist_tracks = self.filter_tracks(tracks_features, vibe)[:20]
        playlist_tracks_data = self.get_tracks_data(
            headers, playlist_tracks, playlist_id
        )
        session["playlist"] = playlist_tracks_data
        return playlist_tracks_data

    def group_track_ids(self, ids, n):
        grouped_list = [ids[i : n + i] for i in range(0, len(ids), n)]
        return grouped_list

    def get_tracks_audio_features(self, headers, ids):
        audio_features = []

        for group in ids:
            string_ids = ",".join(group)
            query = {"ids": string_ids}
            endpoint = self.ENDPOINT_BASE_URL + f"/audio-features?{urlencode(query)}"

            features_data = requests.get(endpoint, headers=headers).json()
            features_list = features_data["audio_features"]

            for track in features_list:
                audio_features.append(
                    {
                        "id": track["id"],
                        "danceability": track["danceability"],
                        "energy": track["energy"],
                        "valence": track["valence"],
                    }
                )

        return audio_features

    def get_tracks_data(self, headers, ids, playlist_id):
        tracks_data = []
        string_ids = ",".join(ids)
        query = {"ids": string_ids}
        endpoint = self.ENDPOINT_BASE_URL + f"/tracks?{urlencode(query)}"

        tracks_data_list = requests.get(endpoint, headers=headers).json()
        for track in tracks_data_list["tracks"]:
            id = track["id"]
            name = track["name"]
            preview_url = track["preview_url"]
            artist = track["artists"][0]["name"]
            album_name = track["album"]["name"]
            album_image_url = track["album"]["images"][0]["url"]

            if not Song.query.filter_by(id=id).first():
                song = Song.create(
                    id, name, preview_url, artist, album_name, album_image_url
                )
            Playlist_Song.create(playlist_id, song.id)

            tracks_data.append(
                {
                    "id": id,
                    "name": name,
                    "preview_url": preview_url,
                    "artist": artist,
                    "album_name": album_name,
                    "album_image_url": album_image_url,
                }
            )
        print("TRACKS DATA", tracks_data)
        return tracks_data

    def filter_tracks(self, tracks_features, vibe):
        spread = Decimal(0.1)
        filtered_tracks = [
            track["id"]
            for track in tracks_features
            if vibe - spread <= track["valence"] <= vibe + spread
        ]
        return filtered_tracks

    def get_new_albums(self, headers):
        new_albums_ids = []
        query = {"limit": 50}
        endpoint = self.ENDPOINT_BASE_URL + f"/browse/new-releases?{urlencode(query)}"

        new_albums_data = requests.get(endpoint, headers=headers).json()
        new_albums_items = new_albums_data["albums"]["items"]

        new_albums_ids = [album["id"] for album in new_albums_items]
        grouped_album_ids = self.group_track_ids(new_albums_ids, 20)

        return grouped_album_ids

    def get_albums_tracks(self, headers, albums_ids):
        tracks = []
        for group in albums_ids:

            string_ids = ",".join(group)
            query = {"ids": string_ids}
            endpoint = self.ENDPOINT_BASE_URL + f"/albums?{urlencode(query)}"

            albums_data = requests.get(endpoint, headers=headers).json()
            albums_list = albums_data["albums"]

            for album in albums_list:
                for track in album["tracks"]["items"]:
                    tracks.append(track["id"])
        shuffle(tracks)
        return tracks


spotify = SpotifyAPI()
