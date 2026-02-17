const LIMIT = 6;
const TOTAL_SONGS = 30;

let offsets = {
    happy: 0,
    calm: 0,
    energetic: 0,
    romantic: 0
};

async function loadSongs(mood) {
    const offset = offsets[mood];

    const res = await fetch(
        `/recommend/${mood}?limit=${LIMIT}&offset=${offset}`
    );

    const data = await res.json();
    const container = document.getElementById("songs");

    // Always replace old songs
    container.innerHTML = "";

    if (!data.tracks || data.tracks.length === 0) {
        return;
    }

    data.tracks.forEach(song => {
        const card = document.createElement("div");
        card.className = "song-card";
        card.innerHTML = `
            <img src="${song.image}" alt="poster">
            <h3>${song.name}</h3>
            <p>${song.artist}</p>
            <button onclick="window.open('${song.spotify_url}')">
                Open in Spotify
            </button>
        `;
        container.appendChild(card);
    });

    // Move to next page
    offsets[mood] += LIMIT;

    // Reset after all 30 songs
    if (offsets[mood] >= TOTAL_SONGS) {
        offsets[mood] = 0;
    }
}
