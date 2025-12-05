"""Tests for the file cleaner module."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cleaner import FileCleaner


class TestFileCleaner(unittest.TestCase):
    """Test cases for FileCleaner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_initialization(self):
        """Test FileCleaner initialization."""
        cleaner = FileCleaner(self.test_dir)
        self.assertEqual(cleaner.directory, self.test_dir)
    
    def test_organize_dry_run(self):
        """Test organize with dry run mode."""
        test_file = self.test_dir / "test.txt"
        test_file.touch()
        
        cleaner = FileCleaner(self.test_dir)
        cleaner.organize(dry_run=True)
        
        self.assertTrue(test_file.exists())


if __name__ == "__main__":
    unittest.main()
