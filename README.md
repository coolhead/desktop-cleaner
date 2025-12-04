Problem: “My desktop turns into a junkyard.”

Solution: desktop_cleaner.py – one command to declutter.

Examples:

python3 desktop_cleaner.py              # clean with autodetect
python3 desktop_cleaner.py --dry-run    # preview only
python3 desktop_cleaner.py --undo       # restore last cleanup


Log Files

Every run writes a timestamped log to ~/.desktop-cleaner/logs/.

Undo Support

--undo restores files using the latest log.
