from pathlib import Path

from arkive.core.drive import Drive
from arkive.drives.local.utils import drive_index, drive_rename, drive_cleanup


class LocalDrive(Drive):
    def index(self, folder: Path):
        assert folder.exists() and folder.is_dir(), \
            f'\'{folder}\' is not a directory.'
        yield from drive_index(folder)

    def rename(self, source: Path, dest: Path):
        drive_rename(source, dest)

    def cleanup(self, folder: Path):
        drive_cleanup(folder)
