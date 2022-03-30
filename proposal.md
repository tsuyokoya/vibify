# Vibify

## Overview:

The goal of this app is to allow music listeners to generate a Spotify playlist of songs based on the user’s indicated mood. 

The user demographic will include:

- music fans
- Spotify users (though not required)

## Data Sources:

The main source of the data will be provided by the [Spotify API](https://developer.spotify.com/documentation/web-api/). Some useful endpoints are:

- ”Get User’s Top Items” / “Get Followed Artists” / “Get Featured Playlists” / “Get New Releases” - may be potential pools of songs from which playlists are created
- “Get Tracks’ Audio Features” - each track has features that can be used to determine its perceived mood / energy (Danceability, Energy, Tempo, Valence)
- “Create Playlist” - create the playlist based on songs determined to fit user mood

## Database Schema:

- users
  - id
  - username
  - password
- playlists
  - id
  - name
  - user_id
- songs
  - id
  - title
  - playlist_id


## Potential API Issues:

- Spotify has a rate limit that is calculated based on the number of calls to its API within a rolling 30 second window. A few endpoints also have custom rate limits that differ from the API-wide rate limit. Rate limit not specified.

## Sensitive Information:

- Encrypted passwords will be stored for the user model.

## Functionality:

- Non-registered users:
  - Can generate a song playlist based on their mood. 
- Registered users:
  - Can generate a song playlist based on their mood. 
  - Can save / add the generated playlist to their own Spotify account after Spotify login.
  - Maybe: allow playlist songs to be played in the app.

## User Flow:

I. Landing page

- Link to register/login
- Slider (or something) to indicate mood / energy (sad, neutral, happy, etc.)
- Textbox to add a name for the playlist
- Button to generate the playlist

II. Playlist page / tab?

- Displays playlist & songs within the playlist
- Displays playlist title
- Displays button to add the playlist to user Spotify account

## Additional Considerations

1. Allow users to save generated playlists in the app
2. Allow users to change username / password
3. Playlist creation based on user mood and additional specifications (specific genre, artist, etc.)
