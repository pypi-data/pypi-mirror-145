import logging
from pathlib import Path

from arkive.core.drive import Drive
from arkive.drives.pcloud.utils import drive_index, drive_mkdir, drive_rename, drive_cleanup

logger = logging.getLogger(__name__)


class PCloudDrive(Drive):
    def __init__(self, auth: dict):
        self.auth = auth

    def index(self, folder: Path):
        logger.info(f'Indexing folder "{folder.as_posix()}".')
        yield from drive_index(folder, self.auth)

    def rename(self, source: Path, dest: Path):
        logger.info(f'Ensuring folder "{dest.parent.as_posix()}" exists.')
        drive_mkdir(dest.parent, self.auth)
        drive_rename(source, dest, self.auth)

    def cleanup(self, folder: Path):
        logger.info(f'Cleaning up folder "{folder.as_posix()}".')
        drive_cleanup(folder, self.auth)
