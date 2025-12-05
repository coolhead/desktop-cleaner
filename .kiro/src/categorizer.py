"""File categorization logic."""

from pathlib import Path
from typing import Dict, List

CATEGORY_MAPPINGS: Dict[str, List[str]] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json"],
    "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
    "Others": []
}


class FileCategorizer:
    """Categorizes files based on their extensions."""
    
    def __init__(self, custom_mappings: Dict[str, List[str]] = None):
        """Initialize the categorizer.
        
        Args:
            custom_mappings: Optional custom category mappings
        """
        self.mappings = custom_mappings or CATEGORY_MAPPINGS
    
    def categorize(self, file_path: Path) -> str:
        """Determine the category for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Category name
        """
        extension = file_path.suffix.lower()
        
        for category, extensions in self.mappings.items():
            if extension in extensions:
                return category
        
        return "Others"
