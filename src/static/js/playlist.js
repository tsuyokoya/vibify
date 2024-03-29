const playlistBtn = document.querySelector("#add-playlist-btn");
const playlistForm = document.querySelector("#add-playlist-form");

const removeActiveSelection = (tracks) => {
  for (track of tracks) {
    if (track.classList.contains("bg-lightGreen")) {
      track.classList.remove("bg-lightGreen");
      track.classList.add("bg-slate-700");
    }
  }
};

window.onload = () => {
  const iframe = document.querySelector("iframe");
  const tracks = document.querySelectorAll(".track");
  const albumImage = document.querySelector("#album-image");
  const baseEmbedURL = "https://open.spotify.com/embed/track/";

  // sets active background color for first track in playlist
  tracks[0].classList.remove("bg-slate-700");
  tracks[0].classList.add("bg-lightGreen");

  tracks.forEach((track) => {
    track.addEventListener("click", (e) => {
      // removes active background color from track
      removeActiveSelection(tracks);

      // sets active background color for selected track
      track.classList.remove("bg-slate-700");
      track.classList.add("bg-lightGreen");

      // updates album image and player url for selected track
      const spotifyId = e.target.attributes["data-id"]["value"];
      iframe.src = baseEmbedURL + spotifyId;
      albumImage.src = e.target.attributes["data-image"]["value"];
    });
  });
};

// Disable submit button after click and add styling
playlistForm.addEventListener("submit", () => {
  playlistBtn.disabled = "true";
  playlistBtn.textContent = "Adding to your Spotify account...";
  playlistBtn.classList.remove(
    "hover:scale-110",
    "hover:bg-black",
    "hover:border-lightGreen",
    "hover:text-lightGreen"
  );
});
