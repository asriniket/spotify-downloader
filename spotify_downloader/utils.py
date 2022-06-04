from urllib.parse import quote

import requests


def get_user_playlists(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    playlists_endpoint = 'https://api.spotify.com/v1/me/playlists/'  # Used to get user's playlists
    playlists = requests.get(playlists_endpoint, headers=headers).json()['items']

    playlists_dict = {'Custom Playlist': 0}
    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        playlists_dict[playlist_name] = playlist_id
    return playlists_dict


def get_album_id(album, headers):
    if 'open.spotify.com/album/' in album:  # If the provided string is a Spotify URL
        album_id = album[album.rindex('/') + 1:]
        if '?' in album_id:  # Remove any URL Parameters from ID String
            album_id = album_id[:album_id.index('?')]
    else:  # If provided string is Spotify search query
        search_endpoint = f'https://api.spotify.com/v1/search?q={quote(album)}&type=album'
        search_results = requests.get(search_endpoint, headers=headers).json()
        album_id = search_results['albums']['items'][0]['id']
    return album_id


def get_playlist_id(playlist):
    if 'open.spotify.com/playlist/' in playlist:  # If the provided string is a Spotify URL
        playlist_id = playlist[playlist.rindex('/') + 1:]
        if '?' in playlist_id:  # Remove any URL Parameters from ID String
            playlist_id = playlist_id[:playlist_id.index('?')]
        return playlist_id
    return None
