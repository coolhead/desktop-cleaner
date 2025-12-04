#!/usr/bin/env python3
"""
Desktop Cleaner – a lazy automation script.

“I hate manually cleaning my messy Desktop,
so I built this to do it for me.”

Features:
- Auto-detect Desktop (Linux/macOS + WSL + Windows via /mnt/c/Users)
- Dry-run mode (no changes)
- Logs every real cleanup to ~/.desktop-cleaner/logs
- Undo last cleanup with --undo
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

# File categories and their extensions
CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".md",
    ],
    "Code": [
        ".py",
        ".ipynb",
        ".js",
        ".ts",
        ".java",
        ".go",
        ".c",
        ".cpp",
        ".rb",
        ".sh",
        ".yaml",
        ".yml",
        ".json",
        ".tf",
    ],
    "Archives": [".zip", ".tar", ".gz", ".tgz", ".rar", ".7z"],
    "Media": [".mp3", ".wav", ".m4a", ".mp4", ".mkv", ".avi", ".mov"],
}


# ---------------------------------------------------------------------------
# Helpers: environment and paths
# ---------------------------------------------------------------------------

def is_wsl() -> bool:
    """Return True if we are running under WSL."""
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        return "microsoft" in platform.release().lower()
    except Exception:
        return False


def candidate_desktops() -> Iterable[Path]:
    """Yield possible Desktop locations in priority order."""
    home = Path.home()

    # Typical Unix/macOS locations
    yield home / "Desktop"
    yield home / "desktop"

    # Some localized names (not exhaustive, but better than nothing)
    for name in ("Escritorio", "Bureau", "Schreibtisch"):
        yield home / name

    # WSL: scan Windows users
    if is_wsl():
        users_root = Path("/mnt/c/Users")
        if users_root.exists():
            for user_dir in users_root.iterdir():
                if user_dir.is_dir():
                    candidate = user_dir / "Desktop"
                    if candidate.exists():
                        yield candidate


def find_desktop(custom_path: str | None) -> Path:
    """
    Detect the user's real Desktop folder.
    Avoids system/public desktops like 'All Users' which are read-only.
    """
    if custom_path:
        p = Path(custom_path).expanduser().resolve()
        if not p.exists():
            raise SystemExit(f"[error] Path does not exist: {p}")
        if not p.is_dir():
            raise SystemExit(f"[error] Not a directory: {p}")
        return p

    candidates = []
    for c in candidate_desktops():
        # Skip known system/public desktops
        blocked = [
            "All Users",
            "Default",
            "Default User",
            "Public",
        ]
        if any(b.lower() in str(c).lower() for b in blocked):
            continue

        if c.exists() and c.is_dir():
            try:
                file_count = sum(1 for x in c.iterdir() if x.is_file())
            except PermissionError:
                continue
            candidates.append((c, file_count))

    if not candidates:
        raise SystemExit(
            "[error] Could not find your Desktop automatically. "
            "Pass --path /mnt/c/Users/<name>/Desktop explicitly."
        )

    # pick user desktop with most files
    candidates.sort(key=lambda t: t[1], reverse=True)
    return candidates[0][0]


# ---------------------------------------------------------------------------
# Core: scan + moves
# ---------------------------------------------------------------------------

def classify_file(path: Path) -> str:
    """Return category name based on file extension."""
    ext = path.suffix.lower()
    for category, exts in CATEGORIES.items():
        if ext in exts:
            return category
    return "Other"


def iter_desktop_files(desktop: Path) -> Iterable[Path]:
    """Yield files that should be organized."""
    for item in desktop.iterdir():
        if item.is_dir():
            # ignore folders; user-created folders stay as-is
            continue
        if item.name.startswith("."):
            # ignore hidden files
            continue
        yield item


def plan_moves(desktop: Path) -> List[Tuple[Path, Path]]:
    """
    Return list of (source_file, target_dir) moves
    without touching the filesystem.
    """
    moves: List[Tuple[Path, Path]] = []
    for src in iter_desktop_files(desktop):
        category = classify_file(src)
        target_dir = desktop / category
        moves.append((src, target_dir))
    return moves


# ---------------------------------------------------------------------------
# Logging + undo
# ---------------------------------------------------------------------------

def get_log_dir() -> Path:
    log_dir = Path.home() / ".desktop-cleaner" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def write_log(desktop: Path, moves: List[Tuple[Path, Path]]) -> Path | None:
    """Write a log file describing the moves: src|dest per line."""
    if not moves:
        return None

    log_dir = get_log_dir()
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = log_dir / f"clean_{ts}.log"

    with log_path.open("w", encoding="utf-8") as f:
        f.write(f"DESKTOP={desktop}\n")
        for src, target_dir in moves:
            dest = target_dir / src.name
            f.write(f"{src}|{dest}\n")

    return log_path


def parse_log(log_path: Path) -> List[Tuple[Path, Path]]:
    """Parse a log file into (src, dest) pairs."""
    moves: List[Tuple[Path, Path]] = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("DESKTOP="):
                continue
            src_str, dest_str = line.split("|", 1)
            moves.append((Path(src_str), Path(dest_str)))
    return moves


def undo_last_run() -> None:
    """Undo the last real cleanup based on the latest log file."""
    log_dir = get_log_dir()
    logs = sorted(log_dir.glob("clean_*.log"))
    if not logs:
        print("[info] No cleanup logs found – nothing to undo.")
        return

    last_log = logs[-1]
    moves = parse_log(last_log)

    if not moves:
        print(f"[info] Log {last_log} contained no moves. Nothing to undo.")
        return

    print(f"[info] Undoing moves from: {last_log}")

    undone = 0
    skipped = 0
    for src, dest in moves:
        if dest.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(src))
            print(f"[undo] {dest.name}  ->  {src.parent}/")
            undone += 1
        else:
            print(f"[skip] Destination missing, cannot undo: {dest}")
            skipped += 1

    print(f"\n[done] Undo complete. {undone} file(s) restored, {skipped} skipped.")


# ---------------------------------------------------------------------------
# Cleaning entrypoint (used by CLI and Streamlit)
# ---------------------------------------------------------------------------

def clean_desktop(desktop: Path, dry_run: bool = False) -> int:
    """
    Execute cleanup:
      - when dry_run=True, only print what would happen.
      - when dry_run=False, move files + write log.

    Returns number of files processed.
    """
    moves = plan_moves(desktop)
    if not moves:
        print("[done] Nothing to clean – your desktop is already zen.")
        return 0

    if dry_run:
        for src, target_dir in moves:
            rel = f"{target_dir.name}/"
            print(f"[dry-run] Would move: {src.name}  ->  {rel}")
        print(f"\n[done] {len(moves)} file(s) would be moved into category folders.")
        return len(moves)

    # Real move
    for src, target_dir in moves:
        target_dir.mkdir(exist_ok=True)
        dest = target_dir / src.name
        shutil.move(str(src), str(dest))
        rel = f"{target_dir.name}/"
        print(f"[moved] {src.name}  ->  {rel}")

    log_path = write_log(desktop, moves)
    if log_path:
        print(f"\n[info] Log written to: {log_path}")
    print(f"[done] {len(moves)} file(s) moved into category folders.")
    return len(moves)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatically organize your Desktop into folders by file type."
    )
    parser.add_argument(
        "--path",
        help=(
            "Desktop path override. "
            "Example on WSL: /mnt/c/Users/<username>/Desktop"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved, but do not actually move any files.",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last cleanup run based on the latest log file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> None:
    args = parse_args(argv)

    if args.undo:
        # Undo does not care about --path or --dry-run
        undo_last_run()
        return

    desktop = find_desktop(args.path)

    print(f"[info] Using desktop folder: {desktop}")
    if args.dry_run:
        print("[info] Running in DRY-RUN mode – no files will be changed.\n")
    else:
        print("[info] Cleaning desktop…\n")

    clean_desktop(desktop, dry_run=args.dry_run)


if __name__ == "__main__":
    main(sys.argv[1:])
