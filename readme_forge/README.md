# 🔨 README Forge

Auto-generate a polished, professional `README.md` for any project — by scanning the actual codebase.

Point it at a directory. It detects your language, framework, entry point, dependencies, license, and project structure, then generates a complete README with proper install instructions, usage commands, and badges. In 2 seconds.

**Because every developer knows they should write a README. Almost nobody does.**

## Features

- 🔍 **Auto-detects** Python, JavaScript/TypeScript, Go, Rust, Java, and more
- 📦 **Framework detection** — Flask, Django, React, Next.js, Vue, Express, Svelte, Spring Boot
- 🏗️ **Generates project structure tree** automatically
- 🐳 **Docker-aware** — adds Docker section if Dockerfile exists
- ⚙️ **CI-aware** — notes GitHub Actions if `.github/workflows` exists
- 📄 **License detection** — reads your LICENSE file and identifies the type
- 🏷️ **Language badges** auto-generated
- 📝 **Proper install/run/test commands** tailored to what it finds
- 👀 **Preview mode** — see the output before committing

## Install

```bash
git clone https://github.com/YOUR_USERNAME/readme-forge.git
cd readme-forge
```

No dependencies required — runs on Python 3.9+ standard library only.

## Usage

Preview a README for the current directory:

```bash
python readme_forge.py
```

Generate for a specific project and save:

```bash
python readme_forge.py /path/to/your/project -o README.md
```

Preview before saving:

```bash
python readme_forge.py /path/to/project -o README.md --preview
```

## Example

Running `readme_forge.py` on a Next.js project might produce:

```markdown
# My Cool App

> A blazing-fast web application

![TypeScript](https://img.shields.io/badge/TypeScript-blue)

## Tech Stack

- **Language(s):** TypeScript
- **Framework:** Next.js
- **Package Manager:** npm

## Installation

    git clone ...
    cd my-cool-app
    npm install

## Usage

    npm run dev
...
```

## What it detects

| Signal | What it means |
|---|---|
| `requirements.txt` / `pyproject.toml` | Python project with pip |
| `package.json` | Node.js, reads scripts and deps |
| `tsconfig.json` | TypeScript variant |
| `go.mod` | Go project |
| `Cargo.toml` | Rust project |
| `pom.xml` / `build.gradle` | Java (Maven/Gradle) |
| `Dockerfile` | Adds Docker section |
| `.github/workflows/` | Notes CI/CD usage |
| `LICENSE` | Detects MIT, Apache, GPL |
| `manage.py` | Django framework |
| `app.py` | Flask framework |
| `next`, `react`, `vue` in deps | Frontend framework |

## Ideas for contributions

- Add Ruby/Rails, PHP/Laravel, and Swift detection
- Generate a `CONTRIBUTING.md` alongside the README
- Table of contents for large projects
- `--style` flag for different README templates (minimal, detailed, badges-heavy)
- Read docstrings from Python entry points for auto-description
- GitHub API integration to auto-fill repo URL and description

## The meta flex

This project's own README was generated using itself. Run `python readme_forge.py . -o README.md` and see.

## Author

Adithyakiran
adithyakiranhere

