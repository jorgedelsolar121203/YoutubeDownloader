# Youtube Downloader

A simple downloader script for YouTube videos and Spotify playlists. It allows you to search for YouTube videos by song name, download them as MP3 files, and also download videos from YouTube playlists and Spotify playlists.

## Features

- **Search and download YouTube videos**: Search for YouTube videos based on song names and download them as MP3 files.
- **Download videos from a YouTube playlist**: Extract video URLs from a YouTube playlist and download all the videos.
- **Download songs from a Spotify playlist**: Extract song names from a Spotify playlist, search them on YouTube, and download the videos as MP3 files.

## Requirements

- Python 3.x
- `yt-dlp` for YouTube video downloading
- `moviepy` for converting videos to MP3
- `spotipy` for interacting with the Spotify API

## Setup

1. Clone the repository or download the script file.
2. Install the required Python libraries:
    ```bash
    pip install yt-dlp moviepy spotipy
    ```

3. Set up your **Spotify API credentials**:
    - Create a Spotify Developer account and create an app [here](https://developer.spotify.com/dashboard/applications).
    - Get your `CLIENT_ID`, `CLIENT_SECRET`, and set the `REDIRECT_URI` (use `http://localhost:8888/callback` as the redirect URI).
    - Replace the placeholders in the script with your credentials:
        ```python
        CLIENT_ID = 'YOUR_CLIENT_ID'
        CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
        REDIRECT_URI = 'http://localhost:8888/callback'
        ```

## Usage

Run the script in your terminal
