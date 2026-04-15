import argparse
import sys
from collections import Counter
from datetime import datetime

import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

API = "https://api.github.com"
console = Console()


def fetch(url: str) -> dict | list:
    """GET a GitHub API URL with friendly error handling."""
    response = requests.get(url, headers={"Accept": "application/vnd.github+json"}, timeout=10)
    if response.status_code == 404:
        console.print(f"[bold red]❌ User not found.[/]")
        sys.exit(1)
    if response.status_code == 403:
        console.print("[bold red]❌ Rate limit hit.[/] Try again in an hour, or set a GITHUB_TOKEN env var.")
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def get_user(username: str) -> dict:
    return fetch(f"{API}/users/{username}")


def get_repos(username: str) -> list[dict]:
    """Fetch all public repos (handles pagination up to 300 repos)."""
    repos = []
    for page in range(1, 4):  # 3 pages × 100 = up to 300 repos
        page_data = fetch(f"{API}/users/{username}/repos?per_page=100&page={page}&sort=updated")
        if not page_data:
            break
        repos.extend(page_data)
    return repos


def calculate_stats(repos: list[dict]) -> dict:
    """Crunch the numbers from a list of repos."""
    own_repos = [r for r in repos if not r["fork"]]
    languages = Counter(r["language"] for r in own_repos if r["language"])
    return {
        "total_repos": len(repos),
        "own_repos": len(own_repos),
        "forked_repos": len(repos) - len(own_repos),
        "total_stars": sum(r["stargazers_count"] for r in own_repos),
        "total_forks": sum(r["forks_count"] for r in own_repos),
        "total_watchers": sum(r["watchers_count"] for r in own_repos),
        "languages": languages,
        "top_repos": sorted(own_repos, key=lambda r: r["stargazers_count"], reverse=True)[:5],
    }


def assign_persona(user: dict, stats: dict) -> tuple[str, str]:
    """Fun classification based on the developer's profile."""
    stars = stats["total_stars"]
    langs = len(stats["languages"])
    repos = stats["own_repos"]
    followers = user["followers"]

    if stars >= 1000 or followers >= 500:
        return "🌟 Open Source Star", "You have a real audience watching your work."
    if langs >= 5:
        return "🦜 Polyglot Hacker", "You speak many languages — fluently."
    if repos >= 30:
        return "🛠️ Prolific Builder", "You ship constantly. Quantity has its own quality."
    if stats["forked_repos"] > stats["own_repos"]:
        return "🔍 Curious Explorer", "You learn by reading other people's code."
    if repos == 0:
        return "👻 Stealth Mode", "Either brand new or working in private. Mysterious."
    return "🌱 Growing Developer", "Building, learning, and putting in the work."


def account_age(created_at: str) -> str:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    days = (datetime.now(created.tzinfo) - created).days
    years, days = divmod(days, 365)
    return f"{years} years, {days} days"


def render_report(user: dict, stats: dict) -> None:
    """Print the gorgeous terminal report."""
    persona, tagline = assign_persona(user, stats)

    # Header
    name = user.get("name") or user["login"]
    bio = user.get("bio") or "[dim]No bio[/]"
    header = Text.assemble(
        (f"{name}", "bold cyan"),
        (f"  @{user['login']}\n", "dim"),
        (f"{bio}\n\n", "italic"),
        (f"{persona}\n", "bold yellow"),
        (f"{tagline}", "dim"),
    )
    console.print(Panel(header, border_style="cyan", expand=False))

    # Account info
    info = Table.grid(padding=(0, 2))
    info.add_column(style="bold")
    info.add_column()
    info.add_row("📍 Location:", user.get("location") or "Unknown")
    info.add_row("🏢 Company:", user.get("company") or "—")
    info.add_row("🔗 Blog:", user.get("blog") or "—")
    info.add_row("📅 Account age:", account_age(user["created_at"]))
    info.add_row("👥 Followers:", f"{user['followers']:,}")
    info.add_row("👤 Following:", f"{user['following']:,}")
    console.print(info)
    console.print()

    # Stats table
    stats_table = Table(title="📊 Repository Stats", show_header=False, border_style="magenta")
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Value", justify="right", style="cyan")
    stats_table.add_row("Public repos", f"{stats['own_repos']}")
    stats_table.add_row("Forked repos", f"{stats['forked_repos']}")
    stats_table.add_row("Total stars earned ⭐", f"{stats['total_stars']:,}")
    stats_table.add_row("Total forks 🍴", f"{stats['total_forks']:,}")
    console.print(stats_table)
    console.print()

    # Top languages
    if stats["languages"]:
        lang_table = Table(title="💻 Top Languages", border_style="green")
        lang_table.add_column("Language", style="bold")
        lang_table.add_column("Repos", justify="right")
        lang_table.add_column("Share", justify="right")
        total = sum(stats["languages"].values())
        for lang, count in stats["languages"].most_common(5):
            share = f"{count / total * 100:.1f}%"
            lang_table.add_row(lang, str(count), share)
        console.print(lang_table)
        console.print()

    # Top repos
    if stats["top_repos"]:
        repo_table = Table(title="🏆 Most Starred Repos", border_style="yellow")
        repo_table.add_column("Name", style="bold cyan")
        repo_table.add_column("Stars ⭐", justify="right")
        repo_table.add_column("Forks 🍴", justify="right")
        repo_table.add_column("Description", style="dim")
        for repo in stats["top_repos"]:
            desc = (repo["description"] or "")[:50]
            if repo["description"] and len(repo["description"]) > 50:
                desc += "…"
            repo_table.add_row(
                repo["name"],
                f"{repo['stargazers_count']:,}",
                f"{repo['forks_count']:,}",
                desc,
            )
        console.print(repo_table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze any GitHub user's public profile.")
    parser.add_argument("username", help="GitHub username to analyze (e.g. 'torvalds')")
    args = parser.parse_args()

    with console.status(f"[cyan]Fetching data for @{args.username}…[/]"):
        user = get_user(args.username)
        repos = get_repos(args.username)
        stats = calculate_stats(repos)

    render_report(user, stats)


if __name__ == "__main__":
    main()
