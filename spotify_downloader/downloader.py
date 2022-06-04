import os

import requests
import yt_dlp
from youtubesearchpython import CustomSearch, VideosSearch, VideoSortOrder


def download_audio(song_artist, song_name, output_folder, filename, file_format):
    # First search for the auto-generated audio (with the "topic" keyword)
    # Get the video with the largest number of views, and see if the song name / artist match
    # If they match, download the song
    # If not, remove the "topic" keyword and repeat the process to find the result with the most views
    # Download the song with the most views
    search_query = f'{song_artist} - {song_name}'
    try:
        video = dict(CustomSearch(f'{search_query} "topic"', VideoSortOrder.viewCount, limit=3).result())['result'][0]
    except IndexError:  # When the "topic" search criteria does not return the appropriate song
        video = dict(VideosSearch(f'{search_query}', limit=3).result())['result'][0]
    # title = video['title']
    # view_count = int(''.join(list(filter(str.isdigit, video['viewCount']['text']))))
    # channel_name = video['channel']['name']
    # print(f'Title: {title}\nid: {id_}\nView Count: {str(view_count)}\nChannel Name: {channel_name}\n')
    id_ = video['id']
    print(f'Downloading {filename}.{file_format}')
    ydl_opts = {
        'quiet': True,
        'noprogress': True,
        'format': 'bestaudio/best',
        'outtmpl': f'../.tmp/{filename}_audio.{file_format}'
    }
    if not os.path.exists(f'../{output_folder}/{filename}.{file_format}'):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={id_}'])
    else:
        print(f'{filename}.{file_format} already exists, skipping.')


def download_cover_art(filename, cover_art_url):
    with open(f'../.tmp/{filename}.jpg', 'wb') as cover_art:
        cover_art.write(requests.get(cover_art_url).content)
