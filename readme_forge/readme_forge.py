import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Files/dirs to always skip when scanning
IGNORE = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".idea", ".vscode", ".mypy_cache", ".pytest_cache",
    "dist", "build", "target", ".next", ".nuxt", "env",
}


def scan_files(root: Path, max_depth: int = 3) -> list[Path]:
    """Recursively collect files, respecting ignore list and depth."""
    results = []

    def _walk(directory: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return
        for entry in entries:
            if entry.name in IGNORE or entry.name.startswith("."):
                continue
            results.append(entry)
            if entry.is_dir():
                _walk(entry, depth + 1)

    _walk(root, 0)
    return results


def detect_project(root: Path, files: list[Path]) -> dict:
    """Analyze the project and return structured metadata."""
    names = {f.name for f in files}
    rel = {str(f.relative_to(root)) for f in files}

    info = {
        "languages": [],
        "framework": None,
        "package_manager": None,
        "entry_point": None,
        "install_cmd": None,
        "run_cmd": None,
        "test_cmd": None,
        "license": None,
        "has_docker": False,
        "has_ci": False,
        "description": None,
    }

    # ── Python ──
    if "requirements.txt" in names or "setup.py" in names or "pyproject.toml" in names:
        info["languages"].append("Python")
        info["package_manager"] = "pip"
        info["install_cmd"] = "pip install -r requirements.txt"

        if "pyproject.toml" in names:
            info["install_cmd"] = "pip install ."

        if "manage.py" in names:
            info["framework"] = "Django"
            info["run_cmd"] = "python manage.py runserver"
        elif "app.py" in names:
            info["framework"] = "Flask"
            info["run_cmd"] = "python app.py"
            info["entry_point"] = "app.py"
        elif "main.py" in names:
            info["entry_point"] = "main.py"
            info["run_cmd"] = "python main.py"

        if "pytest.ini" in names or "conftest.py" in names or "pyproject.toml" in names:
            info["test_cmd"] = "pytest"

    # ── JavaScript / TypeScript ──
    if "package.json" in names:
        lang = "TypeScript" if "tsconfig.json" in names else "JavaScript"
        info["languages"].append(lang)
        info["package_manager"] = "npm"
        info["install_cmd"] = "npm install"

        pkg_path = root / "package.json"
        try:
            pkg = json.loads(pkg_path.read_text())
            scripts = pkg.get("scripts", {})
            info["description"] = pkg.get("description")

            if "dev" in scripts:
                info["run_cmd"] = "npm run dev"
            elif "start" in scripts:
                info["run_cmd"] = "npm start"

            if "test" in scripts:
                info["test_cmd"] = "npm test"

            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                info["framework"] = "Next.js"
            elif "nuxt" in deps:
                info["framework"] = "Nuxt"
            elif "react" in deps:
                info["framework"] = "React"
            elif "vue" in deps:
                info["framework"] = "Vue"
            elif "express" in deps:
                info["framework"] = "Express"
            elif "svelte" in deps:
                info["framework"] = "Svelte"
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # ── Go ──
    if "go.mod" in names:
        info["languages"].append("Go")
        info["package_manager"] = "go modules"
        info["install_cmd"] = "go mod download"
        info["run_cmd"] = "go run ."
        info["test_cmd"] = "go test ./..."

    # ── Rust ──
    if "Cargo.toml" in names:
        info["languages"].append("Rust")
        info["package_manager"] = "cargo"
        info["install_cmd"] = "cargo build"
        info["run_cmd"] = "cargo run"
        info["test_cmd"] = "cargo test"

    # ── Java ──
    if "pom.xml" in names:
        info["languages"].append("Java")
        info["framework"] = "Maven"
        info["install_cmd"] = "mvn install"
        info["run_cmd"] = "mvn spring-boot:run"
        info["test_cmd"] = "mvn test"
    elif "build.gradle" in names:
        info["languages"].append("Java")
        info["framework"] = "Gradle"
        info["install_cmd"] = "./gradlew build"
        info["run_cmd"] = "./gradlew bootRun"
        info["test_cmd"] = "./gradlew test"

    # ── Docker ──
    if "Dockerfile" in names or "docker-compose.yml" in names or "docker-compose.yaml" in names:
        info["has_docker"] = True

    # ── CI ──
    if any(".github/workflows" in str(f) for f in files):
        info["has_ci"] = True

    # ── License ──
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE"):
        if name in names:
            license_text = (root / name).read_text(errors="ignore")[:200].lower()
            if "mit" in license_text:
                info["license"] = "MIT"
            elif "apache" in license_text:
                info["license"] = "Apache 2.0"
            elif "gpl" in license_text:
                info["license"] = "GPL"
            else:
                info["license"] = "See LICENSE file"
            break

    # Fallback language detection by extensions
    ext_map = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".go": "Go", ".rs": "Rust", ".java": "Java",
        ".rb": "Ruby", ".php": "PHP", ".swift": "Swift",
        ".kt": "Kotlin", ".cs": "C#", ".cpp": "C++", ".c": "C",
    }
    for f in files:
        if f.is_file() and f.suffix in ext_map:
            lang = ext_map[f.suffix]
            if lang not in info["languages"]:
                info["languages"].append(lang)

    return info


def build_tree(root: Path, files: list[Path], max_items: int = 30) -> str:
    """Build a simple directory tree string."""
    lines = [f"{root.name}/"]
    shown = 0
    for f in files:
        if shown >= max_items:
            lines.append("    ...")
            break
        rel = f.relative_to(root)
        depth = len(rel.parts) - 1
        indent = "    " * depth
        prefix = "├── " if f != files[-1] else "└── "
        icon = "📁 " if f.is_dir() else ""
        lines.append(f"{indent}{prefix}{icon}{f.name}")
        shown += 1
    return "\n".join(lines)


def generate_readme(root: Path, info: dict, tree: str) -> str:
    """Assemble the full README markdown."""
    project_name = root.resolve().name
    title = project_name.replace("-", " ").replace("_", " ").title()
    lang_badges = " ".join(
        f"![{lang}](https://img.shields.io/badge/{lang}-blue)" for lang in info["languages"]
    )

    sections = []

    # Header
    sections.append(f"# {title}\n")
    if info["description"]:
        sections.append(f"> {info['description']}\n")
    if lang_badges:
        sections.append(f"{lang_badges}\n")

    # Tech stack
    tech = []
    if info["languages"]:
        tech.append(f"**Language(s):** {', '.join(info['languages'])}")
    if info["framework"]:
        tech.append(f"**Framework:** {info['framework']}")
    if info["package_manager"]:
        tech.append(f"**Package Manager:** {info['package_manager']}")
    if tech:
        sections.append("## Tech Stack\n")
        sections.append("\n".join(f"- {t}" for t in tech))
        sections.append("")

    # Project structure
    sections.append("## Project Structure\n")
    sections.append(f"```\n{tree}\n```\n")

    # Prerequisites
    sections.append("## Prerequisites\n")
    if info["languages"]:
        lang = info["languages"][0]
        prereqs = {
            "Python": "- Python 3.9 or higher",
            "JavaScript": "- Node.js 18 or higher\n- npm",
            "TypeScript": "- Node.js 18 or higher\n- npm",
            "Go": "- Go 1.21 or higher",
            "Rust": "- Rust (install via [rustup](https://rustup.rs/))",
            "Java": "- Java 17 or higher",
        }
        sections.append(prereqs.get(lang, f"- {lang} installed"))
    if info["has_docker"]:
        sections.append("- Docker (optional)")
    sections.append("")

    # Installation
    sections.append("## Installation\n")
    sections.append("```bash")
    sections.append(f"git clone https://github.com/YOUR_USERNAME/{project_name}.git")
    sections.append(f"cd {project_name}")
    if info["install_cmd"]:
        sections.append(info["install_cmd"])
    sections.append("```\n")

    # Usage
    if info["run_cmd"]:
        sections.append("## Usage\n")
        sections.append("```bash")
        sections.append(info["run_cmd"])
        sections.append("```\n")

    # Docker
    if info["has_docker"]:
        sections.append("## Docker\n")
        sections.append("```bash")
        sections.append(f"docker build -t {project_name} .")
        sections.append(f"docker run -p 8000:8000 {project_name}")
        sections.append("```\n")

    # Testing
    if info["test_cmd"]:
        sections.append("## Testing\n")
        sections.append("```bash")
        sections.append(info["test_cmd"])
        sections.append("```\n")

    # CI badge
    if info["has_ci"]:
        sections.append("## CI/CD\n")
        sections.append(
            f"This project uses GitHub Actions for continuous integration. "
            f"See the `.github/workflows` directory for pipeline configuration.\n"
        )

    # License
    if info["license"]:
        sections.append("## License\n")
        sections.append(f"This project is licensed under the **{info['license']}** license.\n")

    # Footer
    sections.append("---\n")
    sections.append(f"*README generated by [readme-forge](https://github.com/YOUR_USERNAME/readme-forge) on {datetime.now().strftime('%Y-%m-%d')}*\n")

    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Auto-generate a polished README.md by scanning your project.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Project folder to scan (defaults to current directory)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output path (defaults to stdout; use -o README.md to write directly)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print to terminal even if -o is set (preview mode)",
    )
    args = parser.parse_args()

    root = args.folder.resolve()
    if not root.is_dir():
        print(f"❌ Not a valid directory: {root}")
        sys.exit(1)

    files = scan_files(root)
    info = detect_project(root, files)
    tree = build_tree(root, files)
    readme = generate_readme(root, info, tree)

    if args.preview or args.output is None:
        print(readme)

    if args.output:
        args.output.write_text(readme)
        print(f"\n✅ Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
