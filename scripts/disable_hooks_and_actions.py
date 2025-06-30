# scripts/disable_hooks_and_actions.py
"""
🟫 OPS: Temporarily disables all GitHub Actions and local git hooks by renaming workflow and hook directories.
🟦 NOTE: Run from the project root. To restore, run this script again (it toggles the names).
"""

from pathlib import Path

def toggle_dir(path: Path, disabled_suffix=".disabled"):
    disabled = path.with_name(path.name + disabled_suffix)
    if path.exists():
        # Disable: rename to .disabled
        path.rename(disabled)
        print(f"🟨 CAUTION: Renamed '{path}' to '{disabled}' (disabled).")
    elif disabled.exists():
        # Restore: rename .disabled back to original
        disabled.rename(path)
        print(f"🟩 GOOD: Restored '{path}' from '{disabled}'.")
    else:
        print(f"🟦 NOTE: Neither '{path}' nor '{disabled}' exists. Nothing to do.")

def main():
    repo_root = Path(__file__).resolve().parent.parent
    github_workflows = repo_root / ".github" / "workflows"
    git_hooks = repo_root / ".git" / "hooks"

    print("🟫 OPS: Toggling GitHub Actions workflows and local git hooks...")
    toggle_dir(github_workflows)
    toggle_dir(git_hooks)

    print("\n🟦 NOTE: To restore, run this script again. Only use for temporary bypasses.")

if __name__ == "__main__":
    main()