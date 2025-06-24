import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


def run_command(command, description):
    print(f"--- {description} ---")
    try:
        subprocess.run(command, check=True, cwd=PROJECT_ROOT)
        print(f"--- SUCCESS: {description} ---\n")
    except subprocess.CalledProcessError as e:
        print(
            f"--- ERROR: {description} failed with return code {e.returncode}. ---",
            file=sys.stderr,
        )
        sys.exit(1)
    except FileNotFoundError as e:
        print(
            "--- ERROR: Command not found. Is Poetry installed and on your PATH? ---",
            file=sys.stderr,
        )
        print(f"Error details: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    print("🚀 Starting CodeCraft AI Poetry-based Development Environment Setup...")

    # 🟩 GOOD: Ensure Poetry is installed
    try:
        subprocess.run(
            ["poetry", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "--- ERROR: Poetry is not installed or not found in PATH. ---",
            file=sys.stderr,
        )
        print(
            "Please install Poetry: https://python-poetry.org/docs/#installation",
            file=sys.stderr,
        )
        sys.exit(1)

    # 🟩 GOOD: Install all dependencies (including dev) using Poetry
    run_command(
        ["poetry", "install", "--with", "dev"],
        "Installing all project dependencies with Poetry",
    )

    # 🟩 GOOD: Install pre-commit hooks using Poetry environment
    run_command(
        ["poetry", "run", "pre-commit", "install"],
        "Installing pre-commit hooks for automated quality checks",
    )

    print("✅ Development environment setup is complete!")
    print(
        "   Poetry-managed dependencies are installed and pre-commit hooks are active."
    )
    print("\nTo activate the Poetry shell, run:")
    print("   poetry shell")
    print(
        "Or to run commands in the Poetry environment, prefix with 'poetry run', e.g.:"
    )
    print("   poetry run python your_script.py")


if __name__ == "__main__":
    main()
