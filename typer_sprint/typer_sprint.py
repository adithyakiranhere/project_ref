import argparse
import curses
import random
import time
from dataclasses import dataclass, field
from pathlib import Path

# Passages of varying difficulty — easy to add more
PASSAGES = [
    "The quick brown fox jumps over the lazy dog near the riverbank while the sun sets behind the mountains casting long shadows across the valley below.",
    "Programming is not about typing fast. It is about thinking clearly and solving problems one step at a time. The best code is written slowly and carefully.",
    "In the middle of difficulty lies opportunity. Every bug you encounter is a chance to understand the system more deeply than you did before.",
    "The terminal is where developers feel most at home. No distractions, no fancy buttons, just raw text and the sound of keys clicking in the dark.",
    "Good software is built by people who care about the details. Every function name, every error message, every edge case handled with intention and craft.",
    "Python was created by Guido van Rossum and first released in 1991. It emphasizes code readability and allows programmers to express concepts in fewer lines.",
    "Open source is not just about free software. It is about building things together, sharing knowledge, and trusting strangers to improve what you started.",
    "The best way to learn programming is to build things. Not tutorials, not courses, but real projects that solve real problems you actually care about.",
    "Version control changed everything. The ability to branch, experiment, fail, and roll back gave developers the freedom to be bold without fear of breaking things.",
    "Every expert was once a beginner. The difference is not talent but persistence. Show up every day, write code, read code, and never stop being curious.",
]


@dataclass
class TypingResult:
    """Stores the outcome of a typing test."""
    passage: str
    typed: str
    duration: float
    timestamps: list[float] = field(default_factory=list)

    @property
    def total_chars(self) -> int:
        return len(self.passage)

    @property
    def correct_chars(self) -> int:
        return sum(1 for a, b in zip(self.passage, self.typed) if a == b)

    @property
    def incorrect_chars(self) -> int:
        return self.total_chars - self.correct_chars

    @property
    def accuracy(self) -> float:
        if not self.typed:
            return 0.0
        return (self.correct_chars / self.total_chars) * 100

    @property
    def wpm(self) -> float:
        if self.duration == 0:
            return 0.0
        words = self.correct_chars / 5  # Standard: 1 word = 5 characters
        minutes = self.duration / 60
        return words / minutes

    @property
    def raw_wpm(self) -> float:
        if self.duration == 0:
            return 0.0
        words = len(self.typed) / 5
        minutes = self.duration / 60
        return words / minutes

    @property
    def consistency(self) -> float:
        """Calculate consistency from inter-keystroke intervals."""
        if len(self.timestamps) < 3:
            return 100.0
        intervals = [
            self.timestamps[i] - self.timestamps[i - 1]
            for i in range(1, len(self.timestamps))
        ]
        avg = sum(intervals) / len(intervals)
        if avg == 0:
            return 100.0
        variance = sum((x - avg) ** 2 for x in intervals) / len(intervals)
        std_dev = variance ** 0.5
        cv = std_dev / avg  # Coefficient of variation
        return max(0.0, (1 - cv) * 100)

    def wpm_label(self) -> str:
        w = self.wpm
        if w >= 100:
            return "Blazing Fast"
        if w >= 80:
            return "Professional"
        if w >= 60:
            return "Above Average"
        if w >= 40:
            return "Average"
        if w >= 20:
            return "Learning"
        return "Just Starting"


def run_test(stdscr, passage: str) -> TypingResult:
    """Run the typing test using curses for real-time input."""
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)    # Correct
    curses.init_pair(2, curses.COLOR_RED, -1)       # Wrong
    curses.init_pair(3, curses.COLOR_YELLOW, -1)    # Current cursor
    curses.init_pair(4, curses.COLOR_CYAN, -1)      # UI elements
    curses.init_pair(5, curses.COLOR_WHITE, -1)     # Untyped

    stdscr.clear()
    height, width = stdscr.getmaxyx()
    usable_width = min(width - 4, 80)

    typed_chars = []
    timestamps = []
    start_time = None

    while True:
        stdscr.clear()

        # Header
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(1, 2, "⌨  TYPER SPRINT")
        stdscr.attroff(curses.color_pair(4))
        stdscr.addstr(1, 20, "  Type the text below. Press ESC to quit.")

        # Timer and live WPM
        if start_time and typed_chars:
            elapsed = time.time() - start_time
            live_wpm = (len(typed_chars) / 5) / (elapsed / 60) if elapsed > 0 else 0
            stdscr.addstr(2, 2, f"Time: {elapsed:.1f}s  |  Live WPM: {live_wpm:.0f}  |  {len(typed_chars)}/{len(passage)} chars")

        # Render passage with coloring
        row = 4
        col = 2
        for i, char in enumerate(passage):
            if col >= usable_width + 2:
                row += 1
                col = 2
            if row >= height - 3:
                break

            if i < len(typed_chars):
                if typed_chars[i] == char:
                    stdscr.addstr(row, col, char, curses.color_pair(1) | curses.A_BOLD)
                else:
                    display = typed_chars[i] if typed_chars[i] != " " else "·"
                    stdscr.addstr(row, col, display, curses.color_pair(2) | curses.A_UNDERLINE)
            elif i == len(typed_chars):
                stdscr.addstr(row, col, char, curses.color_pair(3) | curses.A_REVERSE)
            else:
                stdscr.addstr(row, col, char, curses.color_pair(5) | curses.A_DIM)
            col += 1

        # Footer
        stdscr.addstr(height - 2, 2, "ESC: quit  |  Backspace: delete", curses.A_DIM)

        stdscr.refresh()

        # Input handling
        try:
            key = stdscr.getch()
        except KeyboardInterrupt:
            break

        if key == 27:  # ESC
            break

        if key in (curses.KEY_BACKSPACE, 127, 8):
            if typed_chars:
                typed_chars.pop()
                if timestamps:
                    timestamps.pop()
            continue

        if key in (curses.KEY_ENTER, 10, 13):
            continue

        if 32 <= key <= 126:
            if start_time is None:
                start_time = time.time()
            typed_chars.append(chr(key))
            timestamps.append(time.time())

            if len(typed_chars) >= len(passage):
                break

    end_time = time.time()
    duration = (end_time - start_time) if start_time else 0

    return TypingResult(
        passage=passage,
        typed="".join(typed_chars),
        duration=duration,
        timestamps=timestamps,
    )


def show_results(result: TypingResult) -> None:
    """Print the results using Rich for beautiful formatting."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    console = Console()
    console.print()

    # Colored replay of what was typed
    replay = Text()
    for i, char in enumerate(result.passage):
        if i < len(result.typed):
            if result.typed[i] == char:
                replay.append(char, style="bold green")
            else:
                replay.append(result.typed[i], style="bold red underline")
        else:
            replay.append(char, style="dim")

    console.print(Panel(replay, title="Your Typing Replay", border_style="cyan"))

    # Stats table
    stats = Table(show_header=False, border_style="magenta", title="📊 Results")
    stats.add_column("Metric", style="bold")
    stats.add_column("Value", justify="right", style="cyan")

    wpm = result.wpm
    if wpm >= 80:
        wpm_style = "bold green"
    elif wpm >= 50:
        wpm_style = "bold yellow"
    else:
        wpm_style = "bold red"

    stats.add_row("Net WPM", f"[{wpm_style}]{wpm:.1f}[/]")
    stats.add_row("Raw WPM", f"{result.raw_wpm:.1f}")
    stats.add_row("Accuracy", f"{result.accuracy:.1f}%")
    stats.add_row("Consistency", f"{result.consistency:.1f}%")
    stats.add_row("Time", f"{result.duration:.1f}s")
    stats.add_row("Correct / Total", f"{result.correct_chars} / {result.total_chars}")
    stats.add_row("Errors", f"{result.incorrect_chars}")
    stats.add_row("Verdict", result.wpm_label())

    console.print(stats)

    # Fun encouragement
    console.print()
    if wpm >= 100:
        console.print("[bold green]🔥 You're on fire! Insane speed.[/]")
    elif wpm >= 80:
        console.print("[green]⚡ Professional-grade typing. Impressive.[/]")
    elif wpm >= 60:
        console.print("[yellow]👏 Above average! Keep pushing.[/]")
    elif wpm >= 40:
        console.print("[yellow]👍 Solid. Practice will get you higher.[/]")
    else:
        console.print("[cyan]🌱 Everyone starts somewhere. Keep at it![/]")

    console.print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal typing speed test.")
    parser.add_argument(
        "--passage", type=int, default=None,
        help=f"Pick a specific passage (0-{len(PASSAGES) - 1})",
    )
    parser.add_argument
