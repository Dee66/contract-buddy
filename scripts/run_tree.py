import os


def display_tree(start_path="."):
    """
    Generates and prints a customized, architecturally-relevant tree view
    of the project, excluding common noise to focus on structure.
    """
    excluded_dirs = {
        ".git",
        ".venv",
        "venv",
        "ENV",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "cdk.out",
        ".vscode",
    }

    print(f"Architectural Tree View for: {os.path.abspath(start_path)}")
    print("=" * 80)

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Prune the walk by modifying dirs in-place to prevent traversing excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * (level)

        # Print the directory being processed
        dir_name = os.path.basename(root)
        if level == 0:
            # For the root, just print its name
            print(f"{dir_name}/")
        else:
            print(f"{indent[:-4]}└── {dir_name}/")

        sub_indent = " " * 4 * (level + 1)

        # Sort files to ensure consistent output
        files.sort()
        for i, f in enumerate(files):
            is_last = i == len(files) - 1
            connector = "└──" if is_last else "├──"
            print(f"{sub_indent}{connector} {f}")


if __name__ == "__main__":
    display_tree()
