import os


def add_metadata(filename, file_format, metadata):
    metadata_keys = []
    for key in metadata:
        metadata_keys.append(f'-metadata {key}="{metadata[key]}" ')
    os.system(f'ffmpeg -loglevel fatal '
              f'-i ".tmp/{filename}_audio.{file_format}" '
              f'{"".join(metadata_keys)} '
              f'".tmp/{filename}.{file_format}"')


def add_cover_art(output_folder, filename, file_format):
    os.system(f'ffmpeg -loglevel fatal '
              f'-i ".tmp/{filename}.{file_format}" '
              f'-i ".tmp/{filename}.jpg" '
              f'-map 0:0 -map 1:0 -c copy -id3v2_version 3 '
              f'-metadata:s:v title="Album cover" -metadata:s:v comment="Cover (front)" '
              f'"{output_folder}/{filename}.{file_format}"')
