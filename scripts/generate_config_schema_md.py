import sys
import os
from src.adapters.config_manager import AppConfig

"""
Generates a Markdown config schema doc from the AppConfig Pydantic model.
Run this script to keep docs/configuration/config_schema.md in sync with code.
"""

# Ensure the project root is in sys.path for imports like 'src.adapters.config_manager'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

DOC_PATH = "docs/configuration/config_schema.md"


def main():
    schema = AppConfig.schema()
    lines = [
        "# AppConfig Schema",
        "",
        "| Key | Type | Required | Default | Description |",
        "|-----|------|----------|---------|-------------|",
    ]
    for key, prop in schema["properties"].items():
        typ = prop.get("type", "object")
        required = "Yes" if key in schema.get("required", []) else "No"
        default = prop.get("default", "")
        desc = prop.get("description", "")
        lines.append(f"| `{key}` | `{typ}` | {required} | `{default}` | {desc} |")
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {DOC_PATH} from AppConfig model.")


if __name__ == "__main__":
    main()
