from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

PLAYLIST_SERVICE_URL = "http://playlist-service:5004/spotify/playlist"
MOOD_SERVICE_URL = "http://mood-service:8000/predict"

@app.route("/")
def home():
    return render_template("index.html")

# 🔹 EXISTING BUTTON FLOW (DO NOT TOUCH)
@app.route("/recommend/<mood>")
def recommend(mood):
    limit = request.args.get("limit", 6)
    offset = request.args.get("offset", 0)

    res = requests.get(
        f"{PLAYLIST_SERVICE_URL}/{mood}",
        params={"limit": limit, "offset": offset}
    )

    if res.status_code != 200:
        return jsonify({"error": "Playlist service error"}), 500

    return jsonify(res.json())

# 🔹 NEW TEXT-BASED FLOW
@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text")

    # 1️⃣ Mood detection
    mood_res = requests.post(
        MOOD_SERVICE_URL,
        json={"text": text}
    )

    if mood_res.status_code != 200:
        return jsonify({"error": "Mood service failed"}), 500

    mood_data = mood_res.json()
    mood = mood_data["mood"]
    confidence = mood_data["confidence"]

    # 2️⃣ Fetch songs
    playlist_res = requests.get(
        f"{PLAYLIST_SERVICE_URL}/{mood}",
        params={"limit": 6}
    )

    if playlist_res.status_code != 200:
        return jsonify({"error": "Playlist service failed"}), 500

    return jsonify({
        "mood": mood,
        "confidence": confidence,
        "tracks": playlist_res.json()["tracks"]
    })

@app.route("/health")
def health():
    return {"status": "recommender running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
