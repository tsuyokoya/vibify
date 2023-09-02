from datetime import datetime
from flask import (
    flash,
    g,
    Markup,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from random import shuffle

from app.authentication import guest_auth
from app.models import Song
from app.playlist import bp

from ..forms import CreatePlaylistForm
from ..spotify import spotify


@bp.route("/", methods=["GET"])
def show_playlists_page():
    """
    Shows a list of all playlists on user Spotify account
    """

    user_id = g.user.spotify_id
    playlists = spotify.get_user_playlists(user_id)

    playlists_data = playlists[0] if playlists else None
    profile_url = playlists[1] if playlists else None

    return render_template(
        "playlist/playlists.html",
        playlists_data=playlists_data,
        profile_url=profile_url,
    )


@bp.route("/delete", methods=["POST"])
def delete_playlist():
    """
    Delete the selected playlist from Spotify
    """
    playlist_id = request.form.get("playlist_to_delete")
    spotify.unfollow_playlist(playlist_id)
    flash("Deleted playlist", "danger")
    return redirect(url_for("playlist.show_playlists_page"))


@bp.route("/create", methods=["POST"])
def create_custom_playlist():
    form = CreatePlaylistForm()

    if form.validate_on_submit():
        vibe = round(form.vibe.data, 2)
        title = form.title.data

        if not title:
            title = f"my-playlist-{datetime.now().date()}"

        session["title"] = title

        if g.user:
            spotify.create_user_playlist(vibe)
        else:
            guest_auth.authorize()
            spotify.create_user_playlist(vibe)

        return render_template("playlist/new-playlist.html", title=title)


@bp.route("/<title>", methods=["GET"])
def show_preset_playlist(title):
    """
    Creates a playlist with the chosen vibe for user.
    Playlists are generated using existing songs in the database if user is a guest.
    """

    if title == "preset-sad":
        vibe = 0.10
    elif title == "preset-neutral":
        vibe = 0.50
    else:
        vibe = 1.00

    session["title"] = title

    if g.user:
        spotify.create_user_playlist(vibe)
        return render_template("playlist/new-playlist.html")
    else:
        songs = Song.query.filter(Song.valence.between(vibe - 0.15, vibe + 0.15)).all()
        shuffle(songs)
        return render_template("playlist/preset-playlist-guest.html", songs=songs[:15])


@bp.route("/<title>/add-playlist", methods=["POST"])
def add_playlist_to_spotify(title):
    if g.user:
        user_id = g.user.spotify_id
        playlist_info = spotify.create_empty_spotify_playlist(user_id)
        playlist_id = playlist_info["id"]
        playlist_url = playlist_info["external_urls"]["spotify"]

        uris = [track["uri"] for track in session["playlist"]]

        spotify.populate_playlist(playlist_id, uris)

        flash(
            Markup(
                f"<a href='{playlist_url}' target='_blank' class='text-deepPurple underline'>Successfully added playlist to Spotify</a>"
            ),
            "success",
        )

        return redirect("/playlist")
