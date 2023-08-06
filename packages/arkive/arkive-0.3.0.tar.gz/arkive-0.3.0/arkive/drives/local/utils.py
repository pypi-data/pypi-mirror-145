import logging
from pathlib import Path

from tinytag.tinytag import TinyTag, TinyTagException

logger = logging.getLogger(__name__)


def get_track_metadata(item, track):
    return {'artist': track.artist, 'album': track.album, 'title': track.title, 'path': item}


def drive_index(folder: Path):
    for item in folder.rglob('*'):
        if item.is_file():
            try:
                track = TinyTag.get(item)
                yield get_track_metadata(item, track)
            except TinyTagException:
                pass


def drive_rename(file: Path, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    file.replace(output)


def drive_remove(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        pass


def drive_cleanup(folder: Path):
    for item in folder.glob("*"):
        if item.is_dir():
            drive_cleanup(item)
            drive_remove(item)
