# desktop-cleaner

A small Python tool that keeps your Desktop clean by organizing files into folders by type, with **dry-run** and **undo** support.

## Features

- Auto-detect any target folder (works great for Desktop)
- Categorize files into:
  - `Images/`
  - `Documents/`
  - `Code/`
  - `Others/`
- `--dry-run` to preview moves without changing anything
- `--undo` to revert the last cleanup using a history file
- Detailed logging of every action

## Project layout

```text
src/
  main.py          # CLI entrypoint
  cleaner.py       # Core organizing logic
  categorizer.py   # File type detection
  logger.py        # Logging setup
  undo.py          # Undo engine
tests/
  ...pytest tests...

