"""Tests for the file categorizer module."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from categorizer import FileCategorizer


class TestFileCategorizer(unittest.TestCase):
    """Test cases for FileCategorizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.categorizer = FileCategorizer()
    
    def test_categorize_image(self):
        """Test categorization of image files."""
        file_path = Path("test.jpg")
        category = self.categorizer.categorize(file_path)
        self.assertEqual(category, "Images")
    
    def test_categorize_document(self):
        """Test categorization of document files."""
        file_path = Path("test.pdf")
        category = self.categorizer.categorize(file_path)
        self.assertEqual(category, "Documents")
    
    def test_categorize_unknown(self):
        """Test categorization of unknown file types."""
        file_path = Path("test.xyz")
        category = self.categorizer.categorize(file_path)
        self.assertEqual(category, "Others")


if __name__ == "__main__":
    unittest.main()
