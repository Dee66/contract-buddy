"""
Script to scan all .py files under src/ and fix relative imports to be absolute from the project root.
- Changes lines like: from utils.utils import foo  --> from src.utils.utils import foo
- Only rewrites files if changes are made.
- Prints a summary of all changes.
"""

import os
import re

SRC_ROOT = "src"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def fix_import_line(line):
    # Only fix imports that start with from/import and not already using src.
    patterns = [
        (r"^from\s+([a-zA-Z_][\w\.]*)\s+import\s+", r"from src.\1 import "),
        (r"^import\s+([a-zA-Z_][\w\.]*)", r"import src.\1"),
    ]
    # Don't touch lines that already use src.
    if "from src." in line or "import src." in line:
        return line, False
    for pat, repl in patterns:
        m = re.match(pat, line)
        if m:
            # Only fix if the import is not a standard library or third-party (heuristic: must exist as a folder in src/)
            mod = m.group(1).split(".")[0]
            if os.path.isdir(os.path.join(PROJECT_ROOT, SRC_ROOT, mod)):
                new_line = re.sub(pat, repl, line)
                return new_line, True
    return line, False

def process_file(filepath):
    changed = False
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        new_line, did_change = fix_import_line(line)
        if did_change:
            changed = True
        new_lines.append(new_line)
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    return changed

def main():
    changed_files = []
    for root, dirs, files in os.walk(SRC_ROOT):
        for fname in files:
            if fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                if process_file(fpath):
                    changed_files.append(fpath)
    if changed_files:
        print("Updated imports in:")
        for f in changed_files:
            print("  ", f)
    else:
        print("No import changes needed.")

if __name__ == "__main__":
    main()