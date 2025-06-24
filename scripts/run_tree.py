import os
from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "ENV",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "cdk.out",
    ".vscode",
    ".idea",
    ".mypy_cache",
    ".tox",
    ".cache",
    ".history",
    ".ipynb_checkpoints",
    "dist",
    "build",
    ".aws-sam",
    ".serverless",
    "logs",
    "outputs",
    "artifacts",
}

EXCLUDED_FILE_EXTENSIONS = {
    ".pyc",
    ".log",
    ".tmp",
    ".swp",
    ".DS_Store",
}

EXCLUDED_FILE_NAMES = {
    ".env",
    ".gitignore",
    ".dockerignore",
    "Pipfile.lock",
    "poetry.lock",
    "yarn.lock",
    "package-lock.json",
}


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") and part != "." for part in path.parts)


def should_exclude_dir(dirname: str) -> bool:
    return dirname in EXCLUDED_DIRS or dirname.startswith(".")


def should_exclude_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1]
    return (
        filename in EXCLUDED_FILE_NAMES
        or ext in EXCLUDED_FILE_EXTENSIONS
        or filename.startswith(".")
        or filename.endswith("~")
    )


def display_tree(start_path=".", max_depth=3):
    """
    Prints a clean, architecturally-relevant tree view of the project,
    excluding noise and focusing on files/folders useful for debugging,
    architectural review, and Clean Architecture discussions.
    """
    start_path = Path(start_path).resolve()
    print(f"\nArchitectural Tree View for: {start_path}")
    print("=" * 80)

    def walk(current_path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            print(f"{prefix}└── ... (depth limit reached)")
            return

        entries = [
            e
            for e in sorted(
                current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
            )
            if not is_hidden(e)
            and not (e.is_dir() and should_exclude_dir(e.name))
            and not (e.is_file() and should_exclude_file(e.name))
        ]

        for idx, entry in enumerate(entries):
            connector = "└──" if idx == len(entries) - 1 else "├──"
            if entry.is_dir():
                print(f"{prefix}{connector} {entry.name}/")
                walk(
                    entry,
                    prefix + ("    " if idx == len(entries) - 1 else "│   "),
                    depth + 1,
                )
            else:
                print(f"{prefix}{connector} {entry.name}")

    print(f"{start_path.name}/")
    walk(start_path)

    print("\nLegend:")
    print("  [dir]/   = directory")
    print("  file     = file")
    print(
        "  (excluded: hidden/system/lock/log/tmp files, venvs, caches, node_modules, logs, outputs, artifacts, etc.)"
    )
    print("=" * 80)


if __name__ == "__main__":
    # Use the improved, filtered tree by default
    display_tree(".", max_depth=3)
