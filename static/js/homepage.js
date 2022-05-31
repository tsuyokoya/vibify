const playlistTitleInput = document.querySelectorAll(".vibify-inputs")[0];
const playlistVibeInput = document.querySelectorAll(".vibify-inputs")[1];
const playlistTitle = document.querySelector("#playlist-title");
const playlistVibe = document.querySelector("#playlist-vibe");

// Update Playlist Title on cassette image based on user input
playlistTitleInput.addEventListener("input", (e) => {
  const val = e.target.value;
  console.log(val);
  if (val === "") {
    playlistTitle.innerText = "Playlist Title";
  } else {
    playlistTitle.innerText = val;
  }
});

// Update Playlist Vibe emoji on cassette image based on user input
playlistVibeInput.addEventListener("change", (e) => {
  const val = e.target.value;
  if (val <= 2) {
    playlistVibe.innerText = "Vibe: So Sad 😭";
  } else if (val <= 4) {
    playlistVibe.innerText = "Vibe: A little sad 🥲";
  } else if (val <= 6) {
    playlistVibe.innerText = "Vibe: Neutral 😐";
  } else if (val <= 8) {
    playlistVibe.innerText = "Vibe: A little happy 😀";
  } else {
    playlistVibe.innerText = "Vibe: So Happy 😆";
  }
});
