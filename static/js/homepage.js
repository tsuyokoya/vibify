const playlistTitleInput = document.querySelectorAll(".vibify-inputs")[0];
const playlistVibeInput = document.querySelectorAll(".vibify-inputs")[1];
const playlistTitle = document.querySelector("#playlist-title");
const playlistVibe = document.querySelector("#playlist-vibe");

// Update Playlist Title on cassette image based on user input
playlistTitleInput.addEventListener("input", (e) => {
  const val = e.target.value;
  if (val === "") {
    playlistTitle.innerText = "My Playlist Title";
  } else {
    playlistTitle.innerText = val;
  }
});

// Update Playlist Vibe emoji on cassette image based on user input
playlistVibeInput.addEventListener("input", (e) => {
  const val = e.target.value;
  if (val <= 0.2) {
    playlistVibe.innerText = "😭";
  } else if (val <= 0.4) {
    playlistVibe.innerText = "🥲";
  } else if (val <= 0.6) {
    playlistVibe.innerText = "😐";
  } else if (val <= 0.8) {
    playlistVibe.innerText = "😀";
  } else {
    playlistVibe.innerText = "😆";
  }
});
