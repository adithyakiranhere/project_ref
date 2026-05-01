"""By adithyakiranhere"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Map file extensions to category folder names.
# Add/remove extensions freely — this is the heart of the config.
CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Videos":    {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Archives":  {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code":      {".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".html", ".css", ".json", ".yml", ".yaml"},
    "Installers":{".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"},
    "Ebooks":    {".epub", ".mobi", ".azw3"},
}

LOG_FILE = ".organizer_log.json"  # Hidden log inside the target folder


def categorize(extension: str) -> str:
    """Return the category name for a file extension, or 'Others' if unknown."""
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def unique_destination(dest: Path) -> Path:
    """If dest exists, append a number so we never overwrite files."""
    if not dest.exists():
        return dest
    stem, suffix, parent = dest.stem, dest.suffix, dest.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool) -> list[dict]:
    """Organize files in `folder` into category subfolders. Returns move log."""
    if not folder.exists() or not folder.is_dir():
        print(f"❌ Not a valid folder: {folder}")
        sys.exit(1)

    moves = []
    files = [f for f in folder.iterdir() if f.is_file() and f.name != LOG_FILE]

    if not files:
        print("✨ Folder is already clean — nothing to organize.")
        return moves

    print(f"\n📂 Scanning: {folder}")
    print(f"Found {len(files)} file(s)\n")

    for file in files:
        category = categorize(file.suffix)
        category_dir = folder / category
        dest = unique_destination(category_dir / file.name)

        action = "Would move" if dry_run else "Moving"
        print(f"  {action}: {file.name}  →  {category}/")

        if not dry_run:
            category_dir.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest))
            moves.append({"from": str(dest), "to": str(file)})  # reversed for undo

    if dry_run:
        print("\n🔍 Dry run complete. Re-run without --dry-run to apply changes.")
    else:
        print(f"\n✅ Organized {len(moves)} file(s).")

    return moves


def save_log(folder: Path, moves: list[dict]) -> None:
    """Save move log so we can undo later."""
    if not moves:
        return
    log_path = folder / LOG_FILE
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "moves": moves,
    }
    log_path.write_text(json.dumps(log_entry, indent=2))
    print(f"📝 Log saved to {log_path.name}")


def undo(folder: Path) -> None:
    """Read the log and move files back to where they came from."""
    log_path = folder / LOG_FILE
    if not log_path.exists():
        print("❌ No log found — nothing to undo.")
        sys.exit(1)

    data = json.loads(log_path.read_text())
    moves = data.get("moves", [])

    print(f"↩️  Undoing {len(moves)} move(s) from {data['timestamp']}...\n")
    for move in moves:
        src = Path(move["from"])
        dst = Path(move["to"])
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"  Restored: {src.name}")

    log_path.unlink()
    print(f"\n✅ Undo complete. Log cleared.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize a messy folder by file type — safely.",
    )
    parser.add_argument("folder", type=Path, help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without moving any files")
    parser.add_argument("--undo", action="store_true",
                        help="Undo the last organize operation in this folder")
    args = parser.parse_args()

    if args.undo:
        undo(args.folder)
        return

    moves = organize(args.folder, dry_run=args.dry_run)
    if not args.dry_run:
        save_log(args.folder, moves)


if __name__ == "__main__":
    main()
