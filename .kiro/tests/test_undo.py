"""Tests for the undo manager module."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from undo import UndoManager


class TestUndoManager(unittest.TestCase):
    """Test cases for UndoManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.undo_manager = UndoManager()
        self.temp_dir = TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_record_move(self):
        """Test recording a file move."""
        source = Path("source.txt")
        destination = Path("dest.txt")
        
        self.undo_manager.record_move(source, destination)
        self.assertEqual(len(self.undo_manager.history), 1)
    
    def test_undo_empty_history(self):
        """Test undo with empty history."""
        result = self.undo_manager.undo_last()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
