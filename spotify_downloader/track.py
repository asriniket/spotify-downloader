import os

from . import downloader, ffmpeg


class Track:
    def __init__(self, name, artists, album, release_date, disc_number, track_number, album_track_count, genre,
                 cover_art):
        self.name = name
        self.artists = artists
        self.album_artist = self.artists[0]
        self.album = album
        self.release_date = release_date
        self.disc_number = disc_number
        self.track_number = track_number
        self.album_track_count = album_track_count
        self.genre = genre
        self.cover_art = cover_art
        self.filename = ''.join(char for char in self.name if char.isalnum())

    def download(self, file_format, output_folder):
        if not os.path.exists(f'{output_folder}'):
            os.mkdir(f'{output_folder}')
        downloader.download_audio(self.album_artist, self.name, self.album, output_folder, self.filename, file_format)
        downloader.download_cover_art(self.filename, self.cover_art)
        metadata = {
            'title': self.name,
            'artist': ', '.join(self.artists[:]),
            'album_artist': self.album_artist,
            'date': self.release_date,
            'album': self.album,
            'disc': self.disc_number,
            'track': f'{str(self.track_number)})/{str(self.album_track_count)}',
            'genre': self.genre
        }
        ffmpeg.add_metadata(self.filename, file_format, metadata)
        ffmpeg.add_cover_art(output_folder, self.filename, file_format)

    def __str__(self):
        return f'Name: {self.name}\nArtists: {self.artists}\nAlbum Artist: {self.album_artist}\nAlbum: {self.album}\n' \
               f'Release Date: {self.release_date}\nDisc Number: {self.disc_number}\nTrack Number: ' \
               f'{self.track_number}\nGenre: {self.genre}\nCover Art: {self.cover_art}\n'
