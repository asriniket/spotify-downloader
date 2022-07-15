import os
import shutil

import requests

from .track import Track


class Playlist:
    def __init__(self, id_, access_token):
        self.headers = {'Authorization': f'Bearer {access_token}'}
        self.endpoint = f'https://api.spotify.com/v1/playlists/{id_}'
        self.data = requests.get(self.endpoint, headers=self.headers).json()
        self.name = self.data['name']
        self.num_tracks = self.data['tracks']['total']
        self.track_list = []
        self.genre_seeds = self._get_genre_seeds(self.headers)
        self.playlist_genres = {}  # Stores album artist and genre to avoid making excessive API Calls

    def _get_tracks(self):
        for item in self.data['tracks']['items']:
            track = item['track']
            name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            album_artist_id = track['artists'][0]['id']  # For use in getting song genre
            album = track['album']['name']
            release_date = track['album']['release_date']
            disc_number = track['disc_number']
            track_number = track['track_number']
            album_track_count = track['album']['total_tracks']
            genre = self._get_genre(self.headers, artists[0], album_artist_id)
            cover_art = track['album']['images'][0]['url']
            self.track_list.append(Track(name, artists, album, release_date, disc_number, track_number,
                                         album_track_count, genre, cover_art))

    def _get_genre(self, headers, album_artist, album_artist_id):
        # Used to get a song's genre from a given song's album artist. Genres are provided in the form of "genre seeds",
        # that must then be processed to get a genre
        if album_artist in self.playlist_genres.keys():
            return self.playlist_genres[album_artist]

        artists_endpoint = f'https://api.spotify.com/v1/artists/{album_artist_id}'
        data = requests.get(artists_endpoint, headers=headers).json()

        artist_name = data['name']
        artist_genres = data['genres']

        genre = ''
        for artist_genre in artist_genres:
            artist_genre_formatted = artist_genre.replace(' ', '-')
            if '&' in artist_genre_formatted:
                genre = 'R&B'
                break
            for genre_seed in self.genre_seeds:
                if genre_seed in artist_genre_formatted:
                    genre = genre_seed.title().replace('-', ' ')
                    break
        self.playlist_genres[artist_name] = genre
        return None if genre == '' else genre

    def _get_genre_seeds(self, headers):
        genre_seeds_endpoint = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        self.genre_seeds = requests.get(genre_seeds_endpoint, headers=headers).json()['genres']
        return self.genre_seeds

    def download_tracks(self):
        self._get_tracks()
        if not os.path.exists('.tmp'):
            os.mkdir('.tmp')
        print(f'Downloading tracks in: "{self.name}"')
        for track in self.track_list:
            track.download('mp3', self.name)  # self.name refers to the playlist's name
        shutil.rmtree('.tmp')
        print(f'Playlist "{self.name}" download complete')

    def __str__(self):
        return f'Name: {self.name}\nOwner: {self.data["owner"]["display_name"]}\n' \
               f'Description: {self.data["description"]}\n' \
               f'Number of Tracks: {self.num_tracks}\nNumber of Followers: {self.data["followers"]["total"]}\n'
