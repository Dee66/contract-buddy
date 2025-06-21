import os


def list_project_directories(root_dir="."):
    """
    Walks the project directory and prints a clean tree of subdirectories,
    excluding common hidden or generated folders.
    """
    print(f"Inspecting directory structure from: {os.path.abspath(root_dir)}\n")

    excluded_dirs = {
        ".git",
        ".venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        "cdk.out",
    }

    for dirpath, dirnames, _ in os.walk(root_dir, topdown=True):
        # Modify dirnames in-place to prevent os.walk from traversing them
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]

        # Calculate indentation level
        level = dirpath.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * level

        # Print the directory name
        if level > 0:  # Don't print the root directory itself, just its contents
            print(f"{indent}└── {os.path.basename(dirpath)}/")


if __name__ == "__main__":
    list_project_directories()
