#!/usr/bin/env bash

# 🟫 OPS: Unified, production-grade developer workflow for commit and push with pre-commit/pre-push checks.
# 🟦 NOTE: Automates environment setup, hook installation, and ensures all git operations use the Poetry-managed environment.
# 🟪 ARCH: AWS-native, clean architecture, cross-platform, and frictionless for all contributors.

set -e
HOOKS_INSTALLED_MARKER=".git/hooks/.precommit_hooks_installed"

# --- Ensure Poetry is installed ---
if ! command -v poetry >/dev/null 2>&1; then
    echo "🟥 CRITICAL: Poetry is not installed. Please install Poetry: https://python-poetry.org/docs/#installation"
    exit 1
fi

# --- Ensure Poetry environment and dependencies are present ---
if ! poetry env info -p >/dev/null 2>&1; then
    echo "🟦 NOTE: Creating Poetry environment and installing dependencies..."
    poetry install
fi

if ! poetry run pre-commit --version >/dev/null 2>&1; then
    echo "🟦 NOTE: Installing pre-commit in Poetry environment..."
    poetry add --dev pre-commit
fi

# --- Ensure hooks are installed and executable (idempotent, but skip if already installed) ---
if [ ! -f "$HOOKS_INSTALLED_MARKER" ] || [ ! -x ".git/hooks/pre-commit" ] || [ ! -x ".git/hooks/pre-push" ]; then
    poetry run pre-commit install --hook-type pre-commit --hook-type pre-push >/dev/null 2>&1 || true
    if [ -d .git/hooks ]; then
        for hook in .git/hooks/pre-commit .git/hooks/pre-push; do
            [ -f "$hook" ] && chmod +x "$hook"
            [ -f "$hook" ] && dos2unix "$hook" 2>/dev/null || true
        done
    fi
    touch "$HOOKS_INSTALLED_MARKER"
fi

case "$1" in
    commit)
        shift
        # Automatically stage all changes before running hooks and committing
        git add .

        # 🟦 NOTE: Run pre-commit hooks (auto-fix) after staging
        if ! poetry run pre-commit run --all-files; then
            echo "🟨 CAUTION: Pre-commit hooks made changes or failed. Staging all changes for review."
            git add .
            echo "🟦 NOTE: Code was auto-fixed by hooks and staged."
            echo "🟦 ACTION: Please review the changes (git diff), then re-run this script to commit."
            exit 1
        fi

        # 🟦 NOTE: Only proceed if there are staged changes
        if git diff --cached --quiet; then
            echo "🟦 No staged changes to commit."
            exit 0
        fi

        if [ -z "$1" ]; then
            read -rp "🟦 Enter your commit message: " commit_msg
            if [ -z "$commit_msg" ]; then
                echo "🟥 CRITICAL: Commit message cannot be empty."
                exit 1
            fi
            if ! poetry run git commit -m "$commit_msg"; then
                echo "🟥 CRITICAL: Commit failed."
                exit 1
            fi
        else
            if ! poetry run git commit "$@"; then
                echo "🟥 CRITICAL: Commit failed."
                exit 1
            fi
        fi

        # 🟩 GOOD: Automatically pull latest changes with rebase after commit (no prompt)
        echo "🟦 Pulling latest changes with 'git pull --rebase' before push..."
        if ! git pull --rebase; then
            echo "🟥 CRITICAL: Pull (rebase) failed. Resolve conflicts before pushing."
            exit 1
        fi

        # 🟦 NOTE: Prompt to push after commit (default: yes)
        read -rp "🟦 Commit successful. Would you like to push now? [Y/n]: " push_now
        push_now=${push_now:-Y}
        if [[ "$push_now" =~ ^[Yy]$ ]]; then
            if ! poetry run git push; then
                echo "🟥 CRITICAL: Push failed."
                exit 1
            fi
        else
            echo "🟦 Skipping push. You can push later with: bash scripts/dev-git.sh push"
        fi
        ;;
    push)
        shift
        if ! poetry run git push "$@"; then
            echo "🟥 CRITICAL: Push failed."
            exit 1
        fi
        ;;
    *)
        echo "🟦 Usage:"
        echo "  bash scripts/dev-git.sh commit           # Interactive commit message prompt"
        echo "  bash scripts/dev-git.sh commit -m 'msg'  # Standard commit"
        echo "  bash scripts/dev-git.sh push             # Push with checks"
        exit 1
        ;;
esac
