import requests
from urllib.parse import urlencode
from flask import session, g
from decimal import Decimal
from random import shuffle
from models import db, Song, Playlist_Song

from authentication import auth


class SpotifyAPI:
    ENDPOINT_BASE_URL = "https://api.spotify.com/v1"

    def get_user_spotify_data(self):
        """Returns data from user's Spotify account"""
        lookup_url = self.ENDPOINT_BASE_URL + "/me"
        headers = session["headers"]

        user_data = requests.get(lookup_url, headers=headers)
        return user_data.json()

    def create_user_playlist(self, vibe):
        """Creates playlist based on indicated vibe"""
        headers = auth.get_api_access_headers()

        # Get list of ids for the 50 of the newest album releases
        new_albums_ids = self.get_new_albums(headers)
        # Get ids for each track in the newest albums
        track_ids = self.get_albums_tracks(headers, new_albums_ids)
        # Group track_ids into 100s
        grouped_track_ids = self.group_track_ids(track_ids, 100)
        # Get audio features for each track
        tracks_features = self.get_tracks_audio_features(headers, grouped_track_ids)
        # Filter tracks based on vibe input
        playlist_tracks = self.filter_tracks(tracks_features, vibe)[:20]
        # Get track data for each playlist track
        playlist_tracks_data = self.get_tracks_data(headers, playlist_tracks)

        session["playlist"] = playlist_tracks_data
        return playlist_tracks_data

    def group_track_ids(self, ids, n):
        """Group tracks in arrays of n length"""
        grouped_list = [ids[i : n + i] for i in range(0, len(ids), n)]
        return grouped_list

    def get_tracks_audio_features(self, headers, ids):
        """Get audio features data for each group of track ids"""
        audio_features = []

        for group in ids:
            string_ids = ",".join(group)
            query = {"ids": string_ids}
            endpoint = self.ENDPOINT_BASE_URL + f"/audio-features?{urlencode(query)}"

            features_data = requests.get(endpoint, headers=headers).json()
            features_list = [
                track for track in features_data["audio_features"] if track is not None
            ]

            for track in features_list:
                audio_features.append(
                    {
                        "id": track["id"],
                        "danceability": track["danceability"],
                        "energy": track["energy"],
                        "valence": track["valence"],
                    }
                )
                song = Song.query.filter_by(id=track["id"]).first()
                if song:
                    song.valence = track["valence"]
                    db.session.add(song)
                    db.session.commit()

        return audio_features

    def get_tracks_data(self, headers, ids):
        """Get track data for each track in the generated playlist"""
        tracks_data = []
        string_ids = ",".join(ids)
        query = {"ids": string_ids}
        endpoint = self.ENDPOINT_BASE_URL + f"/tracks?{urlencode(query)}"

        tracks_data_list = requests.get(endpoint, headers=headers).json()

        for track in tracks_data_list["tracks"]:
            id = track["id"]
            name = track["name"]
            uri = track["uri"]
            artist = track["artists"][0]["name"]
            album_name = track["album"]["name"]
            album_image_url = track["album"]["images"][0]["url"]

            if g.user:
                if not Song.query.filter_by(id=id).first():
                    song = Song.create(
                        id, name, uri, artist, album_name, album_image_url
                    )
                    Playlist_Song.create(session["playlist_id"], song.id)

            tracks_data.append(
                {
                    "id": id,
                    "name": name,
                    "uri": uri,
                    "artist": artist,
                    "album_name": album_name,
                    "album_image_url": album_image_url,
                }
            )
        return tracks_data

    def filter_tracks(self, tracks_features, vibe):
        """Filter tracks based on indicated vibe plus/minus spread"""
        spread = Decimal(0.1)
        if vibe < 0.15 or vibe > 0.85:
            spread = Decimal(0.2)
        filtered_tracks = [
            track["id"]
            for track in tracks_features
            if vibe - spread <= track["valence"] <= vibe + spread
        ]
        return filtered_tracks

    def get_new_albums(self, headers):
        """Get list of the 50 newest albums"""
        new_albums_ids = []
        query = {"limit": 50}
        endpoint = self.ENDPOINT_BASE_URL + f"/browse/new-releases?{urlencode(query)}"

        new_albums_data = requests.get(endpoint, headers=headers).json()
        new_albums_items = new_albums_data["albums"]["items"]

        new_albums_ids = [album["id"] for album in new_albums_items]
        grouped_album_ids = self.group_track_ids(new_albums_ids, 20)

        return grouped_album_ids

    def get_albums_tracks(self, headers, albums_ids):
        """Get track id for each track in the newest albums"""
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

    def create_empty_spotify_playlist(self, user_id):
        headers = auth.get_api_access_headers()
        endpoint = self.ENDPOINT_BASE_URL + f"/users/{user_id}/playlists"
        data = {"name": session["title"], "public": False}

        response = requests.post(endpoint, headers=headers, json=data).json()
        return response

    def populate_playlist(self, playlist_id, uris):
        headers = auth.get_api_access_headers()
        string_uris = ",".join(uris)
        query = {"uris": string_uris}
        endpoint = (
            self.ENDPOINT_BASE_URL
            + f"/playlists/{playlist_id}/tracks?{urlencode(query)}"
        )

        response = requests.post(endpoint, headers=headers).json()
        return response

    def get_user_playlists(self, user_id):
        playlists = []
        headers = auth.get_api_access_headers()
        endpoint = self.ENDPOINT_BASE_URL + f"/users/{user_id}/playlists"

        response = requests.get(endpoint, headers=headers).json()

        if response["total"] > 0:
            for item in response["items"]:
                id = item["id"]
                name = item["name"]
                url = item["external_urls"]["spotify"]
                image = "https://media.istockphoto.com/vectors/music-note-icon-vector-illustration-vector-id1175435360?k=20&m=1175435360&s=612x612&w=0&h=1yoTgUwobvdFlNxUQtB7_NnWOUD83XOMZHvxUzkOJJs="

                if len(item["images"]) == 3:
                    image = item["images"][1]["url"]

                playlists.append(
                    {
                        "id": id,
                        "name": name,
                        "url": url,
                        "image": image,
                    }
                )
            playlist_url = response["items"][0]["owner"]["external_urls"]["spotify"]
            return playlists, playlist_url

        return None

    def unfollow_playlist(self, playlist_id):
        headers = auth.get_api_access_headers()
        endpoint = self.ENDPOINT_BASE_URL + f"/playlists/{playlist_id}/followers"

        requests.delete(endpoint, headers=headers)
        return True


spotify = SpotifyAPI()
