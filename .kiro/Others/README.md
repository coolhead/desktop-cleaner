# File Organizer

A Python tool to automatically organize files in a directory by categorizing them based on file extensions.

## Features

- Automatically categorizes files by type (Images, Documents, Videos, Audio, etc.)
- Dry-run mode to preview changes before applying
- Undo functionality to revert file moves
- Comprehensive logging
- Extensible categorization system

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Organize files in a directory:

```bash
python src/main.py /path/to/directory
```

### Dry Run

Preview changes without moving files:

```bash
python src/main.py /path/to/directory --dry-run
```

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── cleaner.py       # File organization logic
│   ├── categorizer.py   # File categorization
│   ├── logger.py        # Logging configuration
│   └── undo.py          # Undo functionality
├── tests/
│   ├── __init__.py
│   ├── test_cleaner.py
│   ├── test_categorizer.py
│   └── test_undo.py
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
```

## File Categories

- **Images**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp
- **Documents**: .pdf, .doc, .docx, .txt, .odt, .rtf
- **Videos**: .mp4, .avi, .mkv, .mov, .wmv, .flv
- **Audio**: .mp3, .wav, .flac, .aac, .ogg, .m4a
- **Archives**: .zip, .rar, .7z, .tar, .gz, .bz2
- **Code**: .py, .js, .java, .cpp, .c, .html, .css, .json
- **Spreadsheets**: .xlsx, .xls, .csv, .ods
- **Others**: All other file types

## Running Tests

```bash
python -m pytest tests/
```

## License

MIT License
