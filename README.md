# Youtube-Spotify-Downloader
**Simple Youtube - Spotify Downloader**

**Description**
This project is a downloader for YouTube videos and Spotify playlist songs. It allows users to search and download YouTube videos based on search terms and download songs from Spotify playlists directly to their device. Additionally, it converts downloaded videos to MP3 audio files.

**Features**
YouTube Video Search and Download: Search for YouTube videos using specific terms, including 'lyrics' versions.
YouTube Playlist Download: Extract all video URLs from a playlist and download them.
Video to MP3 Conversion: Convert downloaded videos to MP3 audio files.
Spotify Integration: Download songs from Spotify playlists and find their YouTube versions.

**Requirements**
Python 3.x
Required libraries:
moviepy==1.0.3
spotipy==2.24.0
yt_dlp==2024.12.6

You can install the required libraries using pip:
pip install moviepy==1.0.3 spotipy==2.24.0 yt_dlp==2024.12.6


**Setup**
Spotify Authentication Configuration:
Create a new project on the Spotify Developer Dashboard to obtain the CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI credentials.

Replace the variables in the code with your credentials.


**Using the Downloader:**
Search and Download a YouTube Video: Run the script and select option 1. Enter a search term and select the desired video to download.
Enter Video URLs to Download: Select option 2 and input the YouTube video URLs separated by commas.
Download All Videos from a YouTube Playlist: Select option 3 and provide the URL of a video in the playlist. The script will extract the URLs and download them.
Download Songs from a Spotify Playlist: Select option 4, enter the Spotify playlist URL, and the script will search for YouTube versions of the playlist's tracks and download them.


**Output Files:**
Downloaded videos are saved in a Videos folder on your system.
Converted MP3 files are saved in a Music folder on your system.


**Contributing**
If you want to contribute to this project, feel free to do so by creating a pull request with your changes.


**License**
This project is licensed under the MIT License. See the LICENSE file for more details.
