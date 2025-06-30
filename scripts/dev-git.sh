#!/usr/bin/env bash

# 🟫 OPS: Unified, production-grade developer workflow for commit and push with pre-commit/pre-push checks.
# 🟦 NOTE: Automates environment setup, hook installation, and ensures all git operations use the Poetry-managed environment.
# 🟪 ARCH: AWS-native, clean architecture, cross-platform, and frictionless for all contributors.

set -e

# --- Always resolve paths relative to the repo root ---
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
HOOKS_INSTALLED_MARKER="$HOOKS_DIR/.precommit_hooks_installed"

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
if [ ! -f "$HOOKS_INSTALLED_MARKER" ] || [ ! -x "$HOOKS_DIR/pre-commit" ] || [ ! -x "$HOOKS_DIR/pre-push" ]; then
    poetry run pre-commit install --hook-type pre-commit --hook-type pre-push >/dev/null 2>&1 || true
    if [ -d "$HOOKS_DIR" ]; then
        for hook in "$HOOKS_DIR/pre-commit" "$HOOKS_DIR/pre-push"; do
            [ -f "$hook" ] && chmod +x "$hook"
            [ -f "$hook" ] && dos2unix "$hook" 2>/dev/null || true
        done
    fi
    touch "$HOOKS_INSTALLED_MARKER"
fi

# --- Main commit+push workflow (default) ---
# Stage all changes
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

# Prompt for commit message
read -rp "🟦 Enter your commit message: " commit_msg
if [ -z "$commit_msg" ]; then
    echo "🟥 CRITICAL: Commit message cannot be empty."
    exit 1
fi
if ! poetry run git commit -m "$commit_msg"; then
    echo "🟥 CRITICAL: Commit failed."
    exit 1
fi

# 🟩 GOOD: Automatically pull latest changes with rebase after commit (no prompt)
echo "🟦 Pulling latest changes with 'git pull --rebase' before push..."
if ! git pull --rebase; then
    echo "🟥 CRITICAL: Pull (rebase) failed. Resolve conflicts before pushing."
    exit 1
fi

# 🟦 NOTE: Automatically push after commit (no prompt)
echo "🟦 Pushing to remote..."
if ! poetry run git push; then
    echo "🟥 CRITICAL: Push failed."
    exit 1
fi

echo "🟩 GOOD: Commit and push complete."
