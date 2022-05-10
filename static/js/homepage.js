const playlist_title_input = document.querySelectorAll(".vibify-inputs")[0];
const playlist_vibe_input = document.querySelectorAll(".vibify-inputs")[1];
const playlist_title = document.querySelector("#playlist-title");
const playlist_vibe = document.querySelector("#playlist-vibe");

// Update Playlist Title on cassette image based on user input
playlist_title_input.addEventListener("keyup", (e) => {
  const val = e.target.value;
  if (val === "") {
    playlist_title.innerText = "Playlist Title";
  } else {
    playlist_title.innerText = val;
  }
});

// Update Playlist Vibe emoji on cassette image based on user input
playlist_vibe_input.addEventListener("change", (e) => {
  const val = e.target.value;
  if (val <= 2) {
    playlist_vibe.innerText = "Vibe: So Sad 😭";
  } else if (val <= 4) {
    playlist_vibe.innerText = "Vibe: A little sad 🥲";
  } else if (val <= 6) {
    playlist_vibe.innerText = "Vibe: Neutral 😐";
  } else if (val <= 8) {
    playlist_vibe.innerText = "Vibe: A little happy 😀";
  } else {
    playlist_vibe.innerText = "Vibe: So Happy 😆";
  }
});
