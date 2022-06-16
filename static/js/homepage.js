const playlistTitleInput = document.querySelectorAll(".vibify-inputs")[0];
const playlistVibeInput = document.querySelectorAll(".vibify-inputs")[1];
const playlistTitle = document.querySelector("#playlist-title");
const playlistVibe = document.querySelector("#playlist-vibe");
const submitBtn = document.querySelector("#submit-btn");
const presets = document.querySelectorAll(".preset");
const playlistForm = document.querySelector("#playlist-form");

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

// Disable playlist form button after submission and add styling
playlistForm.addEventListener("submit", () => {
  submitBtn.disabled = "true";
  submitBtn.textContent = "Generating...";
  submitBtn.classList.remove(
    "hover:scale-110",
    "hover:bg-black",
    "hover:border-lightGreen",
    "hover:text-lightGreen"
  );
});

// Disable preset anchor tag after click and add styling
presets.forEach((preset) => {
  preset.addEventListener("click", (e) => {
    e.target.style.pointerEvents = "none";
    e.target.style.backgroundColor = "#1ED760";
    e.target.textContent = "Generating...";
  });
});
