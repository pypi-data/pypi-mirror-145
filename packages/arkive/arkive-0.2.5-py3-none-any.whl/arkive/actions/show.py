from pathlib import Path

from arkive.core.drive import Drive
from arkive.utility.sanitize import sanitize_label


def show_music_file(file: dict):
    file_tags = (file['artist'], file['album'], file['title'])
    return [sanitize_label(str(tag)) for tag in file_tags]


def show_music_collection(drive: Drive, origin: Path):
    content = []
    for file in drive.index(origin):
        item_row = show_music_file(file)
        content.append(item_row)
    return ['ARTIST', 'ALBUM', 'TITLE'], content
