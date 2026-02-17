from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import base64
import time

load_dotenv()
app = Flask(__name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

PLAYLISTS = {
    "happy": "6Ktw8W5QMjLhZRszIPK4r8",
    "calm": "1tPtNIB8ZLmtlQrY4ZvehJ",
    "energetic": "4eyVdbxQvKJjfnA5m95Z5K",
    "romantic": "7jFgzBzv482Px5sRIxZnrZ"
}

ACCESS_TOKEN = None
TOKEN_EXPIRES_AT = 0


def get_access_token():
    global ACCESS_TOKEN, TOKEN_EXPIRES_AT

    if ACCESS_TOKEN and time.time() < TOKEN_EXPIRES_AT:
        return ACCESS_TOKEN

    auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()

    res = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"}
    )

    token_data = res.json()
    ACCESS_TOKEN = token_data["access_token"]
    TOKEN_EXPIRES_AT = time.time() + token_data["expires_in"] - 60

    return ACCESS_TOKEN


@app.route("/spotify/playlist/<mood>")
def get_playlist(mood):
    if mood not in PLAYLISTS:
        return jsonify({"error": "Invalid mood"}), 400

    limit = int(request.args.get("limit", 6))
    offset = int(request.args.get("offset", 0))

    token = get_access_token()
    playlist_id = PLAYLISTS[mood]

    res = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": limit, "offset": offset}
    )

    data = res.json()
    tracks = []

    for item in data.get("items", []):
        track = item.get("track")
        if not track:
            continue

        tracks.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "preview_url": track["preview_url"],
            "spotify_url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"]
                     if track["album"]["images"] else None
        })

    return jsonify({
        "mood": mood,
        "count": len(tracks),
        "tracks": tracks
    })


@app.route("/health")
def health():
    return {"status": "playlist service running"}
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
