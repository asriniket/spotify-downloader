import os
import shutil

import requests

from .track import Track


def _get_genre(headers, genre_seeds, album_artist_id):
    # Used to get a song's genre from a given song's album artist. Genres are provided in the form of "genre seeds",
    # that must then be processed to get a genre
    artists_endpoint = f'https://api.spotify.com/v1/artists/{album_artist_id}'
    artist_genres = requests.get(artists_endpoint, headers=headers).json()['genres']

    genre = ''
    for artist_genre in artist_genres:
        artist_genre_formatted = artist_genre.replace(' ', '-')
        if '&' in artist_genre_formatted:
            genre = 'R&B'
            break
        for genre_seed in genre_seeds:
            if genre_seed in artist_genre_formatted:
                genre = genre_seed.title().replace('-', ' ')
                break
    return None if genre == '' else genre


def _get_genre_seeds(headers):
    genre_seeds_endpoint = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    return requests.get(genre_seeds_endpoint, headers=headers).json()['genres']


class Album:
    def __init__(self, id_, access_token):
        self.headers = {'Authorization': f'Bearer {access_token}'}
        self.endpoint = f'https://api.spotify.com/v1/albums/{id_}'
        self.data = requests.get(self.endpoint, headers=self.headers).json()
        self.name = self.data['name']
        self.num_tracks = self.data['total_tracks']
        self.release_date = self.data['release_date']
        self.cover_art = self.data['images'][0]['url']
        self.track_list = []
        self.genre = _get_genre(self.headers, _get_genre_seeds(self.headers), self.data['artists'][0]['id'])

    def _get_tracks(self):
        for track in self.data['tracks']['items']:
            name = track['name']
            artists = [artist['name'] for artist in track['artists']]
            disc_number = track['disc_number']
            track_number = track['track_number']
            self.track_list.append(Track(name, artists, self.name, self.release_date, disc_number,
                                         track_number, self.num_tracks, self.genre, self.cover_art))

    def download_tracks(self):
        self._get_tracks()
        if not os.path.exists('.tmp'):
            os.mkdir('.tmp')
        print(f'Downloading tracks in: "{self.name}"')
        for track in self.track_list:
            track.download('mp3', self.name)  # self.name refers to the album's name
        shutil.rmtree('.tmp')
        print(f'Album "{self.name}" download complete')
        pass

    def __str__(self):
        return f'Name: {self.name}\nNumber of Tracks: {self.num_tracks}\nRelease Date: {self.release_date}\n' \
               f'Genre: {self.genre}\nCover Art: {self.cover_art}\n'
