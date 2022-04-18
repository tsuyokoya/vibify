# Vibify

## Overview:

The goal of this app is to allow music listeners to generate a Spotify playlist of songs based on the user’s indicated mood.

The user demographic will include:

- Music fans
- Spotify users (though not required to have a Spotify account)

## Tools:

Flask | Jinja | Flask-WTForms | PostgreSQL | SQLAlchemy | bcrypt

## Data Sources:

The main source of the data will be provided by the [Spotify API](https://developer.spotify.com/documentation/web-api/). Some useful endpoints are:

- ”Get User’s Top Items” / “Get Followed Artists” / “Get Featured Playlists” / “Get New Releases” - may be potential pools of songs from which playlists are created
- “Get Tracks’ Audio Features” - each track has features that can be used to determine its perceived mood / energy (Danceability, Energy, Tempo, Valence). Also contains a "preview_url" that can be used to preview a 30 second snippet of a song.
- “Create Playlist” - create the playlist based on songs determined to fit user mood

## Database Schema:

<img src='./vibify-schema.png' alt='schema screenshot' height='350' width='800'>

- users
  - id: TEXT, PK (uuid)
  - first_name: VARCHAR(25)
  - email: VARCHAR(50), unique
  - password: TEXT (hashed)
- playlists
  - id: TEXT, PK (uuid)
  - name: VARCHAR(25)
  - description: VARCHAR(100)
  - user_id: TEXT, FK
- songs
  - id: TEXT, PK (uuid)
  - title: VARCHAR(50)
  - artist: VARCHAR(50)
  - album: VARCHAR(50)
  - artwork: TEXT
  - preview_url: TEXT
- playlists_songs
  - playlist_id: TEXT, FK
  - song_id: TEXT, FK

## Potential API Issues:

- Spotify has a rate limit that is calculated based on the number of calls to its API within a rolling 30 second window. A few endpoints also have custom rate limits that differ from the API-wide rate limit. Rate limit not specified.
  - Solution: cache data for a certain amount of time to minimize requests using Memcached.

## Sensitive Information:

- Hashed passwords will be stored for the user model.

## Functionality:

- Non-registered users:
  - Ability to view auto-generated playlists based on example moods.
  - Can generate a song playlist based on their mood.
  - Can play the song's 30 second preview on the page
- Additional Features for Registered users:
  - Can save the generated playlist to their own Spotify account after Spotify login.
  - Maybe: allow playlist songs to be played in the app in full, rather than a preview.

## User Flow:

I. Landing page

- Auto-generated playlists based on example moods
- Slider to indicate user mood / energy (sad, neutral, happy, etc.)
- Textbox to add a name for the playlist
- Button to generate the playlist
- Link to register/login

II. Log In / Registration Form

- Log In form:
  - Email and Password
- Registration form:
  - First Name, Email, and Password

III. Playlist page

- Displays playlist & songs in the playlist
- Displays user created playlist title
- Displays button to add the playlist to user Spotify account, if user is logged in
- Displays button to generate a new playlist

## Additional Considerations

1. Allow users to see a list of previously generated playlists in the app
2. Show lyrics of the song that is playing
3. Playlist creation based on user mood and additional specifications (specific genre, artist, etc.)
4. Implement password reset
5. Implement 2 factor authentication
