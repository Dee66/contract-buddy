# scripts/setup-hooks.sh (new)
#!/usr/bin/env bash

# 🟫 OPS: One-time setup for developer workstations and CI/CD runners.
# 🟦 NOTE: Ensures all Git hooks are executable and have LF line endings.

set -e

for hook in .git/hooks/*; do
    [ -f "$hook" ] && chmod +x "$hook"
    [ -f "$hook" ] && dos2unix "$hook" 2>/dev/null || true
done

echo "All hooks are now executable and use LF line endings."
