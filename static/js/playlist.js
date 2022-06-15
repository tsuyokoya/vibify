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

  tracks[0].classList.remove("bg-slate-700");
  tracks[0].classList.add("bg-lightGreen");

  tracks.forEach((track) => {
    track.addEventListener("click", (e) => {
      removeActiveSelection(tracks);
      track.classList.remove("bg-slate-700");
      track.classList.add("bg-lightGreen");
      const spotifyId = e.target.attributes["data-id"]["value"];
      console.log(e.target.attributes);
      iframe.src = baseEmbedURL + spotifyId;

      albumImage.src = e.target.attributes["data-image"]["value"];
    });
  });
};
