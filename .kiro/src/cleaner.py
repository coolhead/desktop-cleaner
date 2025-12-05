"""File cleaning and organizing functionality."""

from pathlib import Path
from categorizer import FileCategorizer
from undo import UndoManager
from logger import setup_logger

logger = setup_logger(__name__)


class FileCleaner:
    """Handles file organization operations."""
    
    def __init__(self, directory: Path):
        """Initialize the file cleaner.
        
        Args:
            directory: Target directory to organize
        """
        self.directory = directory
        self.categorizer = FileCategorizer()
        self.undo_manager = UndoManager()
    
    def organize(self, dry_run: bool = False):
        """Organize files in the directory.
        
        Args:
            dry_run: If True, only preview changes without applying
        """
        logger.info(f"Organizing directory: {self.directory}")
        
        for file_path in self.directory.iterdir():
            if file_path.is_file():
                category = self.categorizer.categorize(file_path)
                target_dir = self.directory / category
                
                if dry_run:
                    logger.info(f"Would move: {file_path.name} -> {category}/")
                else:
                    self._move_file(file_path, target_dir)
    
    def _move_file(self, file_path: Path, target_dir: Path):
        """Move a file to the target directory.
        
        Args:
            file_path: Source file path
            target_dir: Destination directory
        """
        target_dir.mkdir(exist_ok=True)
        destination = target_dir / file_path.name
        
        self.undo_manager.record_move(file_path, destination)
        file_path.rename(destination)
        logger.info(f"Moved: {file_path.name} -> {target_dir.name}/")
