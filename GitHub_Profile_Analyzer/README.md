# 🔍 GitHub Profile Analyzer

A beautiful command-line tool that analyzes any GitHub user's public profile and prints a rich, color-formatted report — top languages, most-starred repos, account age, and a fun "developer persona" classification.

Useful for:
- 👀 **Snooping on your interviewer** before a technical round
- 🤝 Researching maintainers before opening an issue or PR
- 📊 Quantifying your own GitHub journey (or your friend's)
- 🎓 Comparing yourself to legends like `torvalds`, `gvanrossum`, or `tj`

## Demo

```bash
python analyzer.py torvalds
```

![demo](docs/demo.png)

## Features

- 🎨 **Beautiful terminal output** powered by [Rich](https://github.com/Textualize/rich)
- 🚀 **Zero auth required** for basic use (works with the GitHub public API)
- 🦜 **Developer persona classification** — find out if you're a *Polyglot Hacker* or an *Open Source Star*
- 📊 Top 5 languages with usage percentages
- ⭐ Top 5 most-starred repositories
- 📅 Account age, followers, location, company, and bio
- 🛡️ Friendly error handling for missing users and rate limits

## Install

```bash
git clone https://github.com/YOUR_USERNAME/github-profile-analyzer.git
cd github-profile-analyzer
pip install -r requirements.txt
```

## Usage

```bash
python analyzer.py <username>
```

Examples:

```bash
python analyzer.py torvalds
python analyzer.py gvanrossum
python analyzer.py YOUR_OWN_USERNAME
```

## Rate limits

The unauthenticated GitHub API allows 60 requests per hour. If you hit the limit, generate a [personal access token](https://github.com/settings/tokens) and the script will use it automatically:

```bash
export GITHUB_TOKEN=your_token_here
python analyzer.py torvalds
```

(With a token, you get 5,000 requests per hour.)

## Developer personas

The script classifies users into one of these categories based on their public activity:

| Persona | Criteria |
|---|---|
| 🌟 Open Source Star | 1000+ stars or 500+ followers |
| 🦜 Polyglot Hacker | Codes in 5+ languages |
| 🛠️ Prolific Builder | Has 30+ public repos |
| 🔍 Curious Explorer | More forks than original repos |
| 👻 Stealth Mode | No public repos |
| 🌱 Growing Developer | Everyone else |

## Ideas for contributions

- Compare two users side-by-side (`analyzer.py user1 vs user2`)
- Export the report as Markdown or PDF
- Add contribution streak detection
- Cache results locally to avoid hitting rate limits
- Build a Streamlit/Flask web version

## License

MIT
