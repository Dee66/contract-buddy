import sys
import subprocess
import venv
from pathlib import Path

VENV_DIR = "venv"
REQUIREMENTS_IN = "requirements.in"
REQUIREMENTS_OUT = "requirements.txt"
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
VENV_PATH = PROJECT_ROOT / VENV_DIR


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
            "--- ERROR: Command not found. Is the virtual environment configured correctly? ---",
            file=sys.stderr,
        )
        print(f"Error details: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    print("🚀 Starting CodeCraft AI Development Environment Setup...")

    if not VENV_PATH.exists():
        print(f"--- Creating virtual environment in '{VENV_PATH}'... ---")
        venv.create(VENV_PATH, with_pip=True)
        print("--- SUCCESS: Virtual environment created. ---\n")
    else:
        print(
            f"--- Virtual environment already exists at '{VENV_PATH}'. Skipping creation. ---\n"
        )

    if sys.platform == "win32":
        pip_executable = VENV_PATH / "Scripts" / "pip.exe"
        pip_compile_executable = VENV_PATH / "Scripts" / "pip-compile.exe"
        pre_commit_executable = VENV_PATH / "Scripts" / "pre-commit.exe"
    else:
        pip_executable = VENV_PATH / "bin" / "pip"
        pip_compile_executable = VENV_PATH / "bin" / "pip-compile"
        pre_commit_executable = VENV_PATH / "bin" / "pre-commit"

    run_command(
        [str(pip_executable), "install", "--upgrade", "pip", "pip-tools"],
        "Installing/upgrading core packaging tools",
    )

    req_in_path = PROJECT_ROOT / REQUIREMENTS_IN
    req_out_path = PROJECT_ROOT / REQUIREMENTS_OUT

    if req_out_path.exists():
        print(
            f"--- Deleting existing lockfile '{req_out_path.name}' to ensure a clean build. ---"
        )
        req_out_path.unlink()

    compile_command = [
        str(pip_compile_executable),
        "--output-file",
        str(req_out_path),
        str(req_in_path),
    ]
    run_command(compile_command, f"Generating lockfile '{REQUIREMENTS_OUT}'")

    install_command = [str(pip_executable), "install", "-r", str(req_out_path)]
    run_command(install_command, "Installing project dependencies from lockfile")

    pre_commit_command = [str(pre_commit_executable), "install"]
    run_command(
        pre_commit_command, "Installing pre-commit hooks for automated quality checks"
    )

    print("✅ Development environment setup is complete!")
    print("   Dependencies are installed and pre-commit hooks are active.")
    print("\nTo activate the virtual environment, run:")
    if sys.platform == "win32":
        print(f"   .\\{VENV_DIR}\\Scripts\\Activate.ps1")
    else:
        print(f"   source {VENV_DIR}/bin/activate")


if __name__ == "__main__":
    main()
