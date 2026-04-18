# ⌨ Typer Sprint

A beautiful **terminal-based typing speed test** that measures your WPM, accuracy, and consistency — right in your terminal. No browser needed.

Think [monkeytype.com](https://monkeytype.com), but for people who live in the terminal.

## Demo

```
⌨  TYPER SPRINT
Time: 24.3s  |  Live WPM: 72  |  89/142 chars

The terminal is where developers feel most at home.
No distractions, no fancy buttons, just raw text
and the sound of keys clicking in the dark.

────────────────────────────────────────
📊 Results
────────────────────────────────────────
Net WPM          :           68.4
Raw WPM          :           72.1
Accuracy         :          94.8%
Consistency      :          87.2%
Time             :          24.3s
Correct / Total  :       135 / 142
Errors           :              7
Verdict          :   Above Average
────────────────────────────────────────

👏 Above average! Keep pushing.
```

## Features

- ⚡ **Live WPM counter** updates as you type
- 🎨 **Color-coded feedback** — green for correct, red for mistakes, highlighted cursor
- 📊 **Detailed stats** — net WPM, raw WPM, accuracy, consistency, error count
- 🔁 **Consistency score** — measures how steady your rhythm is (not just speed)
- 🎯 **10 built-in passages** from easy to challenging
- 📝 **Custom text support** — type your own passage or load from a file
- 🎭 **Colored replay** — see exactly where you made mistakes after the test
- 🏷️ **Verdict system** — from "Just Starting" to "Blazing Fast"
- 🖥️ **Pure terminal** — works over SSH, in tmux, anywhere curses runs

## Install

```bash
git clone https://github.com/YOUR_USERNAME/typer-sprint.git
cd typer-sprint
pip install -r requirements.txt
```

## Usage

Random passage:

```bash
python typer_sprint.py
```

Pick a specific passage (0-9):

```bash
python typer_sprint.py --passage 3
```

Use your own text:

```bash
python typer_sprint.py --custom "Type this exact sentence as fast as you can."
```

Load from a file:

```bash
python typer_sprint.py --file my_passage.txt
```

## How scores work

| Metric | What it measures |
|---|---|
| **Net WPM** | Speed counting only correct characters (1 word = 5 chars) |
| **Raw WPM** | Total typing speed including mistakes |
| **Accuracy** | Percentage of characters typed correctly |
| **Consistency** | How even your typing rhythm is (low variance = high consistency) |

## Verdict tiers

| WPM | Verdict |
|---|---|
| 100+ | 🔥 Blazing Fast |
| 80-99 | ⚡ Professional |
| 60-79 | 👏 Above Average |
| 40-59 | 👍 Average |
| 20-39 | 🌱 Learning |
| <20 | 🐣 Just Starting |

## Ideas for contributions

- Leaderboard — save scores to a local JSON and show personal bests
- Difficulty levels — easy (common words), medium (sentences), hard (code snippets)
- Code mode — type actual Python/JS code with proper indentation
- Multiplayer — two terminals, same passage, race each other
- History graph — plot WPM over time using Rich or matplotlib
- Theme support — different color schemes

## Note

This uses Python's `curses` module for real-time keystroke capture. It works on macOS and Linux out of the box. On Windows, install `windows-curses`:

```bash
pip install windows-curses
```

## License

MIT
