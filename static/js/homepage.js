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

const loadMessages = [
  "Finding the best songs...",
  "Hold on tight...",
  "Vibing with Spotify...",
  "Getting there...",
];

// Select a random loading message
const setLoadMessage = (loadMessages) => {
  const randomIdx = Math.floor(Math.random() * loadMessages.length);
  const msg = loadMessages[randomIdx];
  submitBtn.textContent = msg;
};

// Disable playlist form button after submission and add styling
playlistForm.addEventListener("submit", () => {
  submitBtn.disabled = "true";

  submitBtn.classList.remove(
    "hover:scale-110",
    "hover:bg-lightGreen",
    "hover:border-white",
    "hover:text-white"
  );
  // Add loading message
  submitBtn.textContent = "Generating...";
  setInterval(() => setLoadMessage(loadMessages), 4000);
});

// Disable preset anchor tag after click and add styling
presets.forEach((preset) => {
  preset.addEventListener("click", (e) => {
    e.target.style.pointerEvents = "none";
    e.target.style.backgroundColor = "#1ED760";
    e.target.textContent = "Generating...";
  });
});
