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



    # ---------- Helpers ----------
    def _destination_for(self, file: Path) -> Path:
        """Return the full destination path for a file."""
        category = get_category(file.suffix)
        return self.target_dir / category / file.name


    def _unique_path(self, path: Path) -> Path:
        """If a file with that name exists, add a numeric suffix."""
        if not path.exists():
            return path

        stem, suffix = path.stem, path.suffix
        counter = 1
        while True:
            new_path = path.with_name(f"{stem}_{counter}{suffix}")
            if not new_path.exists():
                return new_path
            counter += 1


    def _log_summary(self, summary: dict) -> None:
        mode = "DRY-RUN" if summary["dry_run"] else "DONE"
        self.logger.info(
            f"[{mode}] Moved {len(summary['moved'])}, "
            f"skipped {len(summary['skipped'])}"
        )
