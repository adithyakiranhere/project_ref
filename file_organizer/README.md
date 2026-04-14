# 🗂️ Smart File Organizer

A tiny Python tool that cleans up messy folders (like your **Downloads** folder) by sorting files into tidy category subfolders — automatically.

Unlike similar scripts floating around GitHub, this one is **safe by default**:
- 🔍 **Dry-run mode** lets you preview every move before touching a single file
- ↩️ **Built-in undo** — one command restores everything exactly how it was
- 📝 **Every run is logged** to a hidden file so nothing is ever lost
- 🚫 **Never overwrites** — auto-renames conflicts as `file (1).pdf`, `file (2).pdf`, etc.

## Why this exists

Because my Downloads folder had 3,400 files in it and I was too embarrassed to screenshot it.

## Features

- Categorizes files into folders: Images, Videos, Audio, Documents, Spreadsheets, Presentations, Archives, Code, Installers, Ebooks, and Others
- Easy to extend — just add extensions to the `CATEGORIES` dict
- Zero dependencies — uses only Python's standard library
- Safe to run on any folder
- Works on Windows, macOS, and Linux

## Usage

Preview what would happen (recommended first run):

```bash
python file_organizer.py ~/Downloads --dry-run
```

Actually organize the folder:

```bash
python file_organizer.py ~/Downloads
```

Changed your mind? Undo it:

```bash
python file_organizer.py ~/Downloads --undo
```

## Example output

```
📂 Scanning: /home/user/Downloads
Found 23 file(s)

  Moving: report.pdf       →  Documents/
  Moving: vacation.jpg     →  Images/
  Moving: setup.exe        →  Installers/
  Moving: song.mp3         →  Audio/
  Moving: project.zip      →  Archives/
  ...

✅ Organized 23 file(s).
📝 Log saved to .organizer_log.json
```

## Extending it

Want to add new categories? Just edit the `CATEGORIES` dict at the top of `file_organizer.py`:

```python
CATEGORIES = {
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
    # ... your categories
}
```

## Ideas for contributions

- `--by-date` mode to also group files by year/month
- Config file support (`organizer.yaml`)
- Watch mode — monitor a folder and auto-organize new files as they arrive
- A simple GUI with tkinter

## License

MIT — do whatever you want with it.
