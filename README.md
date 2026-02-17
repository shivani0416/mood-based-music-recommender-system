Mood-Based Music Recommender

Microservices Architecture | Dockerized | MSc IT Project

📌 Project Overview

The Spotify Mood-Based Music Recommender System is a microservices-based application that recommends songs based on user mood input.

The system integrates with the Spotify API for music data and is fully containerized using Docker with orchestration through Docker Compose.

This project demonstrates:

Microservices architecture

Third-party API integration

Containerized deployment

Service-to-service communication

Scalable backend design

🏗️ Project Structure
SPOTIFY-APP/
│
├── playlist-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── .dockerignore
│
├── recommender-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   └── venv/
│
└── docker-compose.yml

🎼 Playlist Service (Developed by Me)
Role in System

The Playlist Service is responsible for external API communication.

👉 The Playlist Service is the only service that communicates directly with Spotify for fetching songs.

This design ensures centralized API handling and secure token management.

Responsibilities

Handles OAuth authentication

Manages Spotify access tokens

Sends search queries to Spotify

Fetches playlists and track data

Structures raw API data into JSON

Handles API errors and rate limits

Why Only This Service Talks to Spotify?

Protects API credentials

Prevents duplicate API logic

Improves maintainability

Makes system scalable

Allows independent updates if Spotify API changes

This service acts as the External Data Provider Layer.

🎧 Recommender Service (Developed by Me)
Role in System

The Recommender Service handles business logic and user interaction.

This service:

Accepts mood input from frontend

Calls Playlist Service internally

Applies filtering logic

Returns top recommendations

It does NOT directly interact with Spotify.

Responsibilities

Receives mood (Happy, Calm, Energetic, Romantic, etc.)

Maps mood to audio characteristics

Filters tracks received from Playlist Service

Removes irrelevant songs

Returns curated list of 6 songs

Renders results on frontend

Internal Flow

User → Recommender Service → Playlist Service → Spotify API
Spotify API → Playlist Service → Recommender Service → User

⚙️ Technologies Used

Backend Framework: Flask

API Integration: Spotify Web API

Containerization: Docker

Orchestration: Docker Compose

Version Control: GitHub

Database: SQLite (if applicable)

Language: Python

🔑 Environment Configuration

Inside playlist-service/.env:

CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:5001/callback


⚠️ .env must not be pushed to GitHub.

🚀 Running the Project (Docker Recommended)
Step 1: Make sure Docker is running
Step 2:
docker compose up --build


If images are already pushed to Docker Hub:

docker compose up


Docker will automatically pull them.

🌐 Access Application

Recommender Service (Frontend):

http://localhost:<your-configured-port>


Playlist Service runs internally and is accessed via service name in Docker network.

🔐 Security Practices

Environment-based credential storage

Service isolation using containers

Centralized API access

Docker network isolation

📈 Future Enhancements

ML-based recommendation model

Caching using Redis

Cloud deployment

CI/CD pipeline

PostgreSQL integration

Horizontal scaling of services

📚 Academic Justification

This project fulfills microservices subject requirements by demonstrating:

Service separation

Containerization

Independent deployability

API integration

Scalable system architecture
