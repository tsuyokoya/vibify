# Vibify

<img src='' alt='Vibify homepage' height='350' width='500'>

## 🧐 Project Description

Vibify is an app that allows music listeners to generate a Spotify playlist of songs based on the user’s indicated mood.

### Technologies Used

- Front End: JavaScript, Tailwind CSS
- Back End: Python (Flask) | Flask-WTForms | SQLAlchemy | PostgreSQL | Flask-Migrate

### API

- <a href="https://developer.spotify.com/documentation/web-api/quick-start/">Spotify Web API</a>
<hr>

## How it Works

The backend is implemented with Flask. Once a user submits the playlist form or clicks on one of the preset vibes,
requests are made to the <a href="https://developer.spotify.com/documentation/web-api/quick-start/">Spotify Web API</a>
to retrieve tracks from the newest albums on Spotify.

The resulting tracks are then filtered out to match the vibe (0.0 - 1.0) set by the user. The "valence" attribute of each track
(a measure from 0.0 to 1.0 that describes the musical positiveness of a track) was used to determine whether the track matched the
user's vibe.

The resulting group of tracks are then rendered using Jinja, with JavaScript handling user interactions with the playlist (ie
saving the playlist to Spotify or updating the album image and player to correspond with track selection).

<hr>

## Main Features

- **Informational Section**
  <img src="" alt="Vibify informational section">

  - Concisely describes how a user can create a playlist (through form input or through one of the presets)
  - Emphasizes that a playlist can be created by any user, signed in or not

- **One-click playlist creation with a preset vibe (All users)**
  <img src="" alt="Vibify preset playlist">

  - A playlist can also be generated by selecting one of these preset vibe options

- **Playlist creation through form input (All users)**
  <img src="" alt="Vibify playlist form">

  - Any user can generate a playlist through this form, regardless of login status
    <img src="" alt="Vibify playlist logged in">
  - Non-signed in users can play a 30-second preview of the song
    <img src="" alt="Vibify playlist not logged in">
  - Signed in users can play the entirety of the song and add the playlist to their Spotify account

- **User's Playlists Page (Signed in users only)**
  <img src="" alt="Vibify playlists page">
  - Lists every playlist on the user's Spotify account
  - Option to delete the playlist from user's Spotify account
  <hr>
