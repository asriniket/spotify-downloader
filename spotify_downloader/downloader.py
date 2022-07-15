import os

import requests
import yt_dlp
from youtubesearchpython import CustomSearch, VideosSearch, VideoSortOrder


def search_video_strict(song_artist, song_name, album_name):
    search_query = f'{song_artist} - {song_name} - {album_name}'
    try:
        # Search with the "topic" keyword to search for label-provided songs
        videos = dict(CustomSearch(f'{search_query} "topic"', VideoSortOrder.viewCount, limit=3).result())['result']
    except IndexError:  # When the "topic" search criteria does not return the appropriate song
        videos = dict(CustomSearch(f'{search_query}', VideoSortOrder.viewCount, limit=3).result())['result']

    for video in videos:
        # Return the video id only if the video title contains the song name and is not a music video
        if song_name.lower() in video['title'].lower() and 'video' not in video['title'].lower():
            return video['id']
    else:
        # Return the most relevant search result
        return dict(VideosSearch(f'{search_query}', limit=3).result())['result'][0]['id']


def download_audio(song_artist, song_name, album_name, output_folder, filename, file_format):
    video_id = search_video_strict(song_artist, song_name, album_name)
    print(f'Downloading {song_artist} - {song_name}')
    ydl_opts = {
        'quiet': True,
        'noprogress': True,
        'format': 'bestaudio/best',
        'outtmpl': f'.tmp/{filename}_audio.{file_format}'
    }
    if not os.path.exists(f'{output_folder}/{filename}.{file_format}'):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    else:
        print(f'{filename}.{file_format} already exists, skipping.')


def download_cover_art(filename, cover_art_url):
    with open(f'.tmp/{filename}.jpg', 'wb') as cover_art:
        cover_art.write(requests.get(cover_art_url).content)
