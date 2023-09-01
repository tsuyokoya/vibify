from flask import render_template, redirect, request, session, g, flash, Markup
from random import shuffle

from app.authentication import spotify
from app.models import Song
from app.playlist import bp


@bp.route("/", methods=["GET"])
def show_playlists_page():
    user_id = g.user.spotify_id
    playlists = spotify.get_user_playlists(user_id)

    if playlists:
        playlists_data = playlists[0]
        playlists_url = playlists[1]
        return render_template(
            "playlist/playlists.html",
            playlists_data=playlists_data,
            playlists_url=playlists_url,
        )
    return render_template("playlist/playlists.html")


@bp.route("/", methods=["POST"])
def delete_playlist():
    playlist_id = request.form.get("playlist_to_delete")
    spotify.unfollow_playlist(playlist_id)
    flash("Deleted playlist", "danger")
    return redirect("/playlist")


@bp.route("/<title>", methods=["GET", "POST"])
def show_generated_playlist(title):
    if request.method == "POST" and g.user is not None:
        user_id = g.user.spotify_id
        playlist_info = spotify.create_empty_spotify_playlist(user_id)
        playlist_id = playlist_info["id"]
        playlist_url = playlist_info["external_urls"]["spotify"]

        uris = [track["uri"] for track in session["playlist"]]

        spotify.populate_playlist(playlist_id, uris)
        flash(
            Markup(
                f"Successfully added playlist <a href='{playlist_url}' target='_blank' class='text-deepPurple underline'>HERE</a>"
            ),
            "success",
        )

        return redirect("/playlist")

    vibe = 0.10
    if title == "preset-neutral":
        vibe = 0.50
    elif title == "preset-happy":
        vibe = 1.00

    session["title"] = f"{title}"
    # Create preset playlist for guest user (generate playlist from songs in database)
    if g.user is None:
        songs = Song.query.filter(Song.valence.between(vibe - 0.15, vibe + 0.15)).all()
        shuffle(songs)
        return render_template("playlist/guest-preset-playlist.html", songs=songs[:15])

    # Create preset playlist for logged in user
    user_id = g.user.id
    spotify.create_user_playlist(vibe)

    return render_template("playlist/playlist.html")
