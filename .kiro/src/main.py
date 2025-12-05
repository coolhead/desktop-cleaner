"""Main entry point for the file organizer."""

import argparse
from pathlib import Path
from cleaner import FileCleaner
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main function to run the file organizer."""
    parser = argparse.ArgumentParser(description="Organize files in a directory")
    parser.add_argument("directory", type=str, help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization")
    
    args = parser.parse_args()
    target_dir = Path(args.directory)
    
    if not target_dir.exists():
        logger.error(f"Directory does not exist: {target_dir}")
        return
    
    cleaner = FileCleaner(target_dir)
    
    if args.undo:
        cleaner.undo_manager.undo_all()
    else:
        cleaner.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
