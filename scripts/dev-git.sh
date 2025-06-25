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
# Replace marker logic with:
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
        # 🟦 NOTE: Optionally prompt to stage all changes
        read -rp "🟦 Stage all changes with 'git add .' before commit? [y/N]: " stage_now
        if [ "$stage_now" = "y" ] || [ "$stage_now" = "Y" ]; then
            git add .
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

        read -rp "🟦 Commit successful. Would you like to push now? [y/N]: " push_now
        if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
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
