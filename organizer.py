from pathlib import Path
from datetime import datetime
import shutil

from .rules import get_category
from .logger import setup_logger


class FileOrganizer:

    def __init__(self, target_dir: Path, skip_hidden: bool = True):
        self.target_dir = Path(target_dir).expanduser().resolve()
        self.skip_hidden = skip_hidden
        self.logger = setup_logger()

        if not self.target_dir.exists():
            raise FileNotFoundError(f"Directory not found: {self.target_dir}")
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.target_dir}")

    # ---------- Discovery ----------
    def scan(self):
        """Return a list of files (not folders) in the target directory."""
        files = []
        for item in self.target_dir.iterdir():
            if not item.is_file():
                continue
            if self.skip_hidden and item.name.startswith("."):
                continue
            files.append(item)

        self.logger.info(f"Found {len(files)} file(s) in {self.target_dir}")
        return files
