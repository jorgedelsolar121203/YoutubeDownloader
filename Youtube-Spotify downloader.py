import yt_dlp
import sys
import os
import re
from moviepy.editor import AudioFileClip
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify authentication configuration
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'playlist-read-private'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def search_youtube_video(query):
    """
    Searches for the first video on YouTube that matches the provided search term,
    prioritizing versions with 'lyrics'.
    """   
    query_with_lyrics = f"{query} lyrics"  # Add "lyrics" to the search
    options = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(f"ytsearch:{query_with_lyrics}", download=False)
    if 'entries' in result and result['entries']:
        video_url = result['entries'][0]['url']
        print(f"Video found: {video_url}")
        return video_url
    print("No results found.")
    return None


def extract_playlist_urls(playlist_url):
    """
    Extracts URLs of all videos in a YouTube playlist.
    """
    options = {'quiet': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
    if 'entries' in result and result['entries']:
        video_urls = [entry['url'] for entry in result['entries']]
        print(f"Found {len(video_urls)} videos in the playlist.")
        return video_urls
    print("No videos found in the playlist.")
    return []


def clean_filename(name):
    """
    Cleans the filename to avoid unsupported characters, including emojis and special characters.
    Only allows letters, numbers, spaces, parentheses, hyphens, and underscores.
    """
    # Remove emojis
    name = re.sub(r'[\U00010000-\U0010FFFF]', '', name, flags=re.UNICODE)
    # Remove unsupported characters
    name = re.sub(r'[^a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ\-()_]', '', name)
    # Replace multiple spaces with a single space
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def download_video(url):
    """
    Downloads a YouTube video and converts it to MP3.
    """
    videos_folder = os.path.join(os.path.expanduser("~"), "Videos")
    music_folder = os.path.join(os.path.expanduser("~"), "Music")

    if not os.path.exists(videos_folder):
        print("Videos folder not found on your system.")
        sys.exit(1)
    if not os.path.exists(music_folder):
        print("Music folder not found on your system.")
        sys.exit(1)

    options = {
        'format': 'best',
        'outtmpl': os.path.join(videos_folder, '%(title)s.%(ext)s'),
        'retries': 10,
        'fragment-retries': 10,
        'noplaylist': True,
        'quiet': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            print(f"Downloading video from {url}...")
            info_dict = ydl.extract_info(url, download=True)
            video_title = clean_filename(info_dict['title'])

            # Rename the downloaded file
            original_video_file = os.path.join(videos_folder, f"{info_dict['title']}.mp4")
            cleaned_video_file = os.path.join(videos_folder, f"{video_title}.mp4")

            if os.path.exists(original_video_file):
                os.rename(original_video_file, cleaned_video_file)

            # Convert the downloaded video to MP3
            print(f"Converting {cleaned_video_file} to MP3...")
            audio = AudioFileClip(cleaned_video_file)
            mp3_file = os.path.join(music_folder, f"{video_title}.mp3")
            audio.write_audiofile(mp3_file, codec='mp3')
            print(f"MP3 file saved to {mp3_file}")
            os.remove(cleaned_video_file)

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading the video {url}: {e}")
    except Exception as e:
        print(f"An error occurred while downloading the video {url}: {e}")


def get_playlist_url_from_video(video_url):
    """
    Extracts the playlist URL from a video URL in the playlist.
    """
    match = re.search(r"list=([a-zA-Z0-9_-]+)", video_url)
    if match:
        playlist_url = f"https://www.youtube.com/playlist?list={match.group(1)}"
        print(f"Playlist URL: {playlist_url}")
        return playlist_url
    print("No playlist ID found in the provided URL.")
    return None


def get_spotify_playlist_titles(playlist_id):
    """
    Retrieves the track titles from a Spotify playlist.
    """
    results = sp.playlist_tracks(playlist_id)
    return [track['track']['name'] for track in results['items']]


def show_menu():
    """
    Displays the main menu and manages the selected option by the user.
    """
    print("\nWelcome to the video and song downloader!")
    print("Select an option:")
    print("1) Search and download a YouTube video")
    print("2) Enter video URLs to download")
    print("3) Download all videos from a YouTube playlist")
    print("4) Download songs from a Spotify playlist")

    option = input("Choose an option (1/2/3/4): ").strip()
    return option


def main():
    while True:
        option = show_menu()

        if option == '1':
            query = input("Enter the search term on YouTube: ").strip()
            if query:
                video_url = search_youtube_video(query)
                if video_url:
                    download_video(video_url)

        elif option == '2':
            urls_input = input("Enter the YouTube video URLs (separated by commas): ").strip()
            urls = [url.strip() for url in urls_input.split(",")]
            for url in urls:
                download_video(url)

        elif option == '3':
            playlist_url = input("Enter the YouTube playlist video URL: ").strip()
            playlist_url = get_playlist_url_from_video(playlist_url)
            if playlist_url:
                video_urls = extract_playlist_urls(playlist_url)
                for url in video_urls:
                    download_video(url)

        elif option == '4':
            spotify_playlist_url = input("Enter the Spotify playlist URL: ").strip()
            match = re.search(r"playlist/([a-zA-Z0-9_-]+)", spotify_playlist_url)
            if match:
                playlist_id = match.group(1)
                titles = get_spotify_playlist_titles(playlist_id)
                not_found = []
                for title in titles:
                    video_url = search_youtube_video(title)
                    if video_url:
                        download_video(video_url)
                    else:
                        not_found.append(title)
                if not_found:
                    print("\nNo videos were found for the following titles:")
                    for title in not_found:
                        print(f"- {title}")
            else:
                print("No valid playlist found in the Spotify URL.")
        
        else:
            print("Invalid option. Please try again.")
        
        continue_prompt = input("Would you like to perform another operation? (y/n): ").strip().lower()
        if continue_prompt != 'y':
            print("Thank you for using the downloader. See you next time!")
            break

if __name__ == "__main__":
    main()
