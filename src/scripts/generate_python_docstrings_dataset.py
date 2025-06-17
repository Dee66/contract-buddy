import json
import inspect
import pkgutil
import importlib
import os
import sys
from pathlib import Path
from src.utils.environment import get_mode, setup_logging

def extract_docstrings(module_names, max_per_module=50, min_length=10):
    logging = __import__("logging")
    docs = []
    failed = []
    for name in module_names:
        try:
            module = importlib.import_module(name)
            doc = inspect.getdoc(module)
            if doc and len(doc) >= min_length:
                docs.append({"content": doc})
            count = 0
            for _, member in inspect.getmembers(module):
                if inspect.isfunction(member) or inspect.isclass(member):
                    doc = inspect.getdoc(member)
                    if doc and len(doc) >= min_length:
                        docs.append({"content": doc})
                        count += 1
                if count >= max_per_module:
                    break
        except Exception as e:
            logging.warning(f"Failed to import {name}: {e}")
            failed.append(name)
    return docs, failed

def deduplicate_docs(docs):
    seen = set()
    unique_docs = []
    for d in docs:
        c = d["content"]
        if c not in seen:
            unique_docs.append(d)
            seen.add(c)
    return unique_docs

def main():
    setup_logging()
    logging = __import__("logging")
    mode = get_mode()
    if mode == "dev":
        modules = ["os", "sys", "json", "math", "random"]
        max_per_module = 10
    else:
        # For showcase, you may want to expand this list
        modules = ["os", "sys", "json", "math", "random", "datetime", "re", "collections", "itertools", "functools"]
        max_per_module = 50

    output_path = "data/clean/docs.json"
    Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)

    logging.info(f"Extracting docstrings from modules: {modules} (max {max_per_module} per module)")
    docs, failed = extract_docstrings(modules, max_per_module)
    unique_docs = deduplicate_docs(docs)

    if len(unique_docs) < 2:
        logging.error(f"Only {len(unique_docs)} docstrings found. Pipeline will not proceed.")
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_docs, f, indent=2)
    logging.info(f"Docstring extraction complete: {len(unique_docs)} entries written to {output_path}")

    if failed:
        logging.warning(f"Failed to import {len(failed)} modules: {failed}")

if __name__ == "__main__":
    main()