import os

import requests
import yt_dlp
from youtubesearchpython import CustomSearch, VideosSearch, VideoSortOrder


def search_video_strict(song_artist, song_name, album_name):
    search_query = f'{song_artist} - {song_name} - {album_name}'

    # Search with the "topic" keyword to search for label-provided songs
    videos = dict(CustomSearch(f'{search_query} "topic"', VideoSortOrder.viewCount, limit=3).result())['result']
    if not videos:  # When the "topic" search criteria does not return any songs
        # print('"Topic" keyword returned no results. Changing Search Criteria.')
        videos = dict(VideosSearch(f'{search_query} (Audio)', limit=3).result())['result']
    for video in videos:
        # Return the video id only if the video title contains the song name and is not a music video
        song_name_words = song_name.lower().split()
        video_title = video['title'].lower()

        # Check if the song name is present within the video's title
        for word in song_name_words:
            if word not in video_title:
                break

        if 'video' not in video_title.lower():
            # print(video_title)
            return video['id']
    else:
        # Return top result
        return dict(VideosSearch(f'{search_query} "topic"', limit=1).result())['result'][0]['id']


def download_audio(song_artist, song_name, album_name, output_folder, filename, file_format):
    print(f'Downloading {song_artist} - {song_name}')
    video_id = search_video_strict(song_artist, song_name, album_name)
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
