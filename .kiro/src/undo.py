"""Undo functionality for file operations."""

import json
from pathlib import Path
from typing import List, Tuple
from logger import setup_logger

logger = setup_logger(__name__)


class UndoManager:
    """Manages undo operations for file moves."""
    
    def __init__(self, history_file: Path = None):
        """Initialize the undo manager.
        
        Args:
            history_file: Path to the history file for persistence
        """
        self.history_file = history_file or Path(".file_organizer_history.json")
        self.history: List[Tuple[Path, Path]] = []
        self._load_history()
    
    def _load_history(self):
        """Load history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.history = [(Path(s), Path(d)) for s, d in data]
                logger.info(f"Loaded {len(self.history)} operations from history")
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
    
    def _save_history(self):
        """Save history to file."""
        try:
            data = [[str(s), str(d)] for s, d in self.history]
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def record_move(self, source: Path, destination: Path):
        """Record a file move operation.
        
        Args:
            source: Original file path
            destination: New file path
        """
        self.history.append((source, destination))
        self._save_history()
    
    def undo_last(self) -> bool:
        """Undo the last file move operation.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.history:
            logger.warning("No operations to undo")
            return False
        
        source, destination = self.history.pop()
        
        if destination.exists():
            destination.rename(source)
            logger.info(f"Undone: {destination} -> {source}")
            self._save_history()
            return True
        else:
            logger.error(f"Cannot undo: {destination} does not exist")
            self._save_history()
            return False
    
    def undo_all(self):
        """Undo all recorded file move operations."""
        while self.history:
            self.undo_last()
