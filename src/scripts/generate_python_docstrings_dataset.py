import json
import inspect
import pkgutil
import importlib

def get_stdlib_modules():
    # Get a list of standard library modules (excluding builtins and packages)
    stdlib_modules = []
    for _, name, ispkg in pkgutil.iter_modules():
        if not ispkg and not name.startswith("_"):
            stdlib_modules.append(name)
    return stdlib_modules

def extract_docstrings(module_names, max_per_module=50):
    docs = []
    for name in module_names:
        try:
            module = importlib.import_module(name)
            doc = inspect.getdoc(module)
            if doc:
                docs.append({"content": doc})
            # Extract docstrings from functions/classes in the module
            count = 0
            for _, member in inspect.getmembers(module):
                if inspect.isfunction(member) or inspect.isclass(member):
                    doc = inspect.getdoc(member)
                    if doc:
                        docs.append({"content": doc})
                        count += 1
                if count >= max_per_module:
                    break
        except Exception:
            continue
    return docs

if __name__ == "__main__":
    modules = get_stdlib_modules()
    docs = extract_docstrings(modules, max_per_module=50)
    # Deduplicate
    seen = set()
    unique_docs = []
    for d in docs:
        c = d["content"]
        if c not in seen:
            unique_docs.append(d)
            seen.add(c)
    with open("data/clean/docs.json", "w", encoding="utf-8") as f:
        json.dump(unique_docs, f, indent=2)
    print(f"Saved {len(unique_docs)} docstring chunks to data/clean/docs.json")