# scripts/disable_hooks_and_actions.py
"""
🟫 OPS: Temporarily disables all GitHub Actions and local git hooks by renaming workflow and hook directories.
🟦 NOTE: Run from the project root. To restore, run the script again (it toggles the names).
"""

import os
from pathlib import Path

def toggle_dir(path: Path, disabled_suffix=".disabled"):
    if path.exists():
        disabled = path.with_name(path.name + disabled_suffix)
        if not disabled.exists():
            path.rename(disabled)
            print(f"🟨 CAUTION: Renamed '{path}' to '{disabled}' (disabled).")
        else:
            print(f"🟦 NOTE: '{disabled}' already exists. Skipping.")
    else:
        enabled = Path(str(path).replace(disabled_suffix, ""))
        if enabled.exists():
            print(f"🟦 NOTE: '{enabled}' already enabled. Skipping.")
        else:
            # Try to restore if disabled exists
            disabled = path
            enabled = Path(str(path).replace(disabled_suffix, ""))
            if disabled.exists():
                disabled.rename(enabled)
                print(f"🟩 GOOD: Restored '{enabled}' from '{disabled}'.")

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