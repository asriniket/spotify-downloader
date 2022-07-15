import os
import shutil

from pick import pick

from spotify_downloader import authentication, album, utils, playlist


def cleanup():  # Delete the .tmp folder if it exists
    if os.path.exists('.tmp/'):
        shutil.rmtree('.tmp/')


def main():
    cleanup()
    access_token = authentication.authenticate_user()
    headers = {'Authorization': f'Bearer {access_token}'}

    prompt = 'Would you like to download an album or a playlist? Press Enter to confirm the selection.'
    selection = pick(['Album', 'Playlist'], prompt)[0][0]
    if selection == 'Album':
        album_str = str(input('Please enter the name of the album or the Spotify URL of the album.\n'))
        album_id = utils.get_album_id(album_str, headers)
        album_ = album.Album(album_id, access_token)
        print()
        print(album_)
        album_.download_tracks()
    else:
        user_playlists = utils.get_user_playlists(access_token)
        playlists_prompt = 'Please choose the playlist(s) to be downloaded. ' \
                           'If you would like to download a custom playlist, select the "Custom Playlist" option. ' \
                           'Press Space to select a playlist, and Enter to confirm the selection. '
        selected_playlists = pick(list(user_playlists.keys()), playlists_prompt, multiselect=True,
                                  min_selection_count=1)
        playlist_names, _ = zip(*selected_playlists)
        if 'Custom Playlist' in playlist_names:
            playlist_str = str(input('Please enter the Spotify URL of the playlist.\n'))
            playlist_id = utils.get_playlist_id(playlist_str)
            playlist_ = playlist.Playlist(playlist_id, access_token)
            print()
            print(playlist_)
            playlist_.download_tracks()
        else:
            for selected_playlist in playlist_names:
                playlist_id = user_playlists[selected_playlist]
                playlist_ = playlist.Playlist(playlist_id, access_token)
                print()
                print(playlist_)
                playlist_.download_tracks()
    cleanup()


if __name__ == "__main__":
    main()
