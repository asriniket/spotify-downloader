# Spotify Downloader

Spotify Downloader allows you to download albums and playlists off of Spotify.

# Features

- Easy to use, console-based application
- Supports downloading both user-generated playlists and public playlists
- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp)
  alongside [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) to accurately download audio
  files.

# Installation

### Prerequisites

- [Python](https://www.python.org/downloads/) (version 3.8 or greater)
- pip
- [ffmpeg](https://ffmpeg.org/)

### Steps

1. Clone the repository by running ```git clone URL_TO_REPOSITORY``` or downloading the code as a ZIP file.
2. Run the following code in the command line: `pip install -r requirements.txt`, to install the necessary packages.
3. Within the root folder of the project, create a `secrets.json` file and populate it with the following info:

```
{
"client_id": "[SPOTIFY CLIENT ID]",
"client_secret": "[SPOTIFY CLIENT SECRET]"
}
```

Instructions on how to get a Spotify client ID and secret can be
found [here](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/).

`Application name` and `Application description` fields can be anything you choose, but the `Redirect URIs` field **
must** contain `http://localhost:8080/` in order for the application to function.

# Usage

When all the necessary prerequisites are installed, simply run the `spotify_downloader.py` file to begin downloading
songs.

The first time the program runs, you will be required to authorize the program to access your playlist information.
After authorizing the application, you will be able to see your playlists available for download. 
