import os
import csv
import re
from datetime import datetime
import hashlib
from collections import defaultdict

EXCLUDE_DIRS = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', 'site-packages', 'archive'}

TEMPLATES = {
    "Deliverables.md": """# {section} Deliverables

> **Purpose:** Summarize all deliverables for the {section} phase.

---

## Key Deliverables

- [List or table of deliverables]

---

## Status & Links

- [Link to related docs, logs, or reports]

---

## Last Updated

- {last_updated}
""",
    "README.md": """# {section} Overview

Welcome to the {section} module of Contract Buddy AI.

---

## Purpose

[Brief description of this module's purpose.]

---

## Key Files

- [List of important files]

---

## Navigation

[⬅ Back to Documentation Index](../INDEX.md)

---

## Last Updated

- {last_updated}
"""
}

def is_excluded(path):
    return any(part in EXCLUDE_DIRS for part in path.split(os.sep))

def extract_headings_and_links(filepath):
    headings = []
    links = []
    title = ""
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            heading_match = re.match(r'^(#+)\s+(.*)', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                headings.append(f"{'#' * level} {text}")
                if not title and level == 1:
                    title = text
            for match in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line):
                links.append(match[1])
    return title, headings, links

def summarize_content(filepath, max_chars=200):
    summary = ""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
        content = re.sub(r'#+\s+.*', '', content)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', '', content)
        summary = content.strip().replace('\n', ' ')
        summary = summary[:max_chars]
    return summary

def content_hash(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
        content = re.sub(r'\s+', '', content)
        return hashlib.sha1(content.encode('utf-8')).hexdigest()

def find_markdown_files(root):
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for filename in filenames:
            if filename.lower().endswith('.md'):
                rel_path = os.path.relpath(os.path.join(dirpath, filename), root)
                if not is_excluded(rel_path):
                    full_path = os.path.join(dirpath, filename)
                    try:
                        stat = os.stat(full_path)
                        title, headings, links = extract_headings_and_links(full_path)
                        summary = summarize_content(full_path)
                        hashval = content_hash(full_path)
                        md_files.append({
                            'path': rel_path.replace("\\", "/"),
                            'full_path': full_path,
                            'dir': os.path.dirname(rel_path).replace("\\", "/"),
                            'size_kb': round(stat.st_size / 1024, 2),
                            'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'title': title,
                            'headings': " | ".join(headings),
                            'links': " | ".join(links),
                            'summary': summary,
                            'hash': hashval
                        })
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")
    return md_files

def write_csv(md_files, out_file='markdown_inventory.csv'):
    fieldnames = ['path', 'size_kb', 'last_modified', 'title', 'headings', 'links', 'summary', 'hash']
    with open(out_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for f in md_files:
            row = {k: f[k] for k in fieldnames}
            writer.writerow(row)

def build_navigation_graph(md_files):
    nav_graph = {}
    all_paths = set(f['path'] for f in md_files)
    for f in md_files:
        links = []
        for link in f['links'].split(' | '):
            if link.endswith('.md') and not link.startswith('http'):
                link_path = link.split('#')[0]
                norm_link = os.path.normpath(os.path.join(os.path.dirname(f['path']), link_path)).replace("\\", "/")
                if norm_link in all_paths:
                    links.append(norm_link)
        nav_graph[f['path']] = set(links)
    return nav_graph

def write_mermaid_graph(nav_graph, out_file='docs_nav.mmd'):
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("graph TD\n")
        for src, targets in nav_graph.items():
            for tgt in targets:
                f.write(f'    "{src}" --> "{tgt}"\n')

# --- START OF RESTORED MISSING FUNCTIONS ---

def get_section_anchor(file_path_str):
    """
    Determines the anchor for a file based on its path.
    e.g., 'contract-buddy/docs/foundation/file.md' -> '#foundation'
    """
    match = re.search(r'contract-buddy/docs/([^/]+)/', file_path_str)
    if match:
        return f"#{match.group(1).lower()}"
    return ""

def update_navigation_in_bulk(md_files, index_md_path):
    """
    Updates the 'Back to...' navigation block at the top of each markdown file.
    """
    for md_file in md_files:
        # Skip updating the main index file itself
        if os.path.abspath(md_file['full_path']) == os.path.abspath(index_md_path):
            continue

        file_dir = os.path.dirname(md_file['full_path'])
        
        # 1. Create the link back to the main index, with a section anchor
        rel_to_index = os.path.relpath(index_md_path, file_dir).replace("\\", "/")
        section_anchor = get_section_anchor(md_file['path'])
        index_link = f"{rel_to_index}{section_anchor}"

        # 2. Create the link back to the section overview (README.md) if it exists
        section_readme_path = os.path.join(file_dir, "README.md")
        nav_links = []
        if os.path.isfile(section_readme_path) and os.path.abspath(md_file['full_path']) != os.path.abspath(section_readme_path):
            nav_links.append("[⬅ Back to Section Overview](README.md)")
        
        nav_links.append(f"[⬅ Back to Main Index]({index_link})")
        
        # Create the final navigation block with proper spacing
        nav_block = "\n\n".join(nav_links) + "\n\n"
        
        try:
            with open(md_file['full_path'], 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find where the actual content starts, skipping old nav links and blank lines
            start_idx = 0
            for i, line in enumerate(lines):
                stripped_line = line.strip()
                if not re.match(r'^\[⬅.*\]\(.*\)', stripped_line) and stripped_line != '':
                    start_idx = i
                    break
            else: # If the file is empty or only contains nav links
                start_idx = len(lines)

            # Reconstruct the file with the new nav block
            new_content = nav_block + "".join(lines[start_idx:])
            
            with open(md_file['full_path'], 'w', encoding='utf-8') as f:
                f.write(new_content)

        except Exception as e:
            print(f"  [Warning] Could not update navigation for {md_file['path']}: {e}")

# --- END OF RESTORED MISSING FUNCTIONS ---

# Define the curated structure with descriptions and explicit anchors for the main INDEX.md
CURATED_INDEX_WITH_DESC = {
    "🏛️ Foundation": {
        "anchor": "foundation",
        "description": "Strategic groundwork, architecture, and risk management.",
        "paths": [
            "docs/foundation/Business_Problem_Value.md", "docs/foundation/Architecture_Blueprint.md",
            "docs/foundation/Model_Strategy.md", "docs/foundation/Risk_Constraints.md", "docs/foundation/README.md"
        ]
    },
    "🧠 Core & Optimization": {
        "anchor": "core",
        "description": "Data, pipelines, experimentation, and benchmarking.",
        "paths": [
            "docs/core/Data_Sourcing.md", "docs/core/Data_Pipeline_Processing.md",
            "docs/core/Model_Implementation_Experimentation.md", "docs/core/Benchmarking_Optimization.md", "docs/core/README.md"
        ]
    },
    "🏗️ Build & Readiness": {
        "anchor": "build",
        "description": "APIs, deployment, validation, and monitoring.",
        "paths": [
            "docs/build/API_Integration.md", "docs/build/Deployment_Infrastructure.md",
            "docs/build/Testing_Validation.md", "docs/build/Observability_Monitoring.md", "docs/build/README.md"
        ]
    },
    "🚀 Portfolio & Storytelling": {
        "anchor": "portfolio",
        "description": "Summaries, unique value, and narrative.",
        "paths": [
            "docs/portfolio/Ultimate_README.md", "docs/portfolio/Unique_Value.md",
            "docs/portfolio/Verbal_Narrative.md", "docs/portfolio/README.md"
        ]
    },
    "📊 Reports": {
        "anchor": "reports",
        "description": "Benchmarks, cost tracking, and checklists.",
        "paths": ["docs/BENCHMARKING.md", "docs/COST_TRACKING.md", "docs/checklist.md"]
    },
    "🧩 Data & Embedding": {
        "anchor": "data",
        "description": "Clean data and embedding modules.",
        "paths": ["data/clean/benchmark_report.md", "src/embedding/readme.md"]
    },
    "🏠 Root": {
        "anchor": "root",
        "description": "Project-wide overview and quickstart.",
        "paths": ["Readme.md"]
    }
}

def generate_accordion_navigation(structure, md_files, index_md_path):
    """
    Generates a polished, collapsible HTML accordion navigation with a clean, modern design.
    - Uses a dedicated <a id="..."> tag for robust anchoring.
    """
    file_map = {f['path'].replace('\\', '/'): f for f in md_files}
    lines = ["<!-- NAV_START -->"]
    index_dir = os.path.dirname(index_md_path)
    project_folder = "contract-buddy"

    is_first = True
    for section_title, data in structure.items():
        if not is_first:
            lines.append("\n---")
        
        # Add the robust, empty anchor tag right before the <details> block.
        anchor_id = data.get("anchor", "")
        if anchor_id:
            lines.append(f'<a id="{anchor_id}"></a>')

        details_tag = "<details open>" if is_first else "<details>"
        lines.append(details_tag)
        lines.append(f'  <summary style="font-size: 1.1em; font-weight: 600; cursor: pointer; margin-bottom: 5px;">{section_title}</summary>')
        
        lines.append('  <div style="padding: 10px 15px; border-left: 3px solid #d0d7de; margin-top: 10px; margin-left: 10px;">')
        lines.append(f'  <p><em>{data["description"]}</em></p>')
        
        for path in data["paths"]:
            lookup_path = f"{project_folder}/{path}"
            if lookup_path in file_map:
                info = file_map[lookup_path]
                title = info.get('title') or os.path.splitext(os.path.basename(path))[0].replace('_', ' ')
                link = os.path.relpath(info['full_path'], index_dir).replace('\\', '/')
                lines.append(f'  <p><a href="{link}">{title}</a></p>')
        
        lines.append('  </div>')
        lines.append("</details>")
        is_first = False
        
    lines.append("<!-- NAV_END -->")
    return "\n".join(lines)

def update_index_md_with_markers(index_md_path, nav_section):
    """Replaces content between <!-- NAV_START --> and <!-- NAV_END --> markers."""
    try:
        with open(index_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        start_marker, end_marker = "<!-- NAV_START -->", "<!-- NAV_END -->"
        start_pos, end_pos = content.find(start_marker), content.find(end_marker)

        if start_pos != -1 and end_pos != -1:
            pre = content[:start_pos]
            post = content[end_pos + len(end_marker):]
            new_content = pre + nav_section + post
            with open(index_md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            print("[Error] Navigation markers not found in INDEX.md. Update aborted.")
    except Exception as e:
        print(f"Error updating INDEX.md: {e}")

# --- REPLACE THE MAIN EXECUTION BLOCK ---

if __name__ == '__main__':
    # Use the script's directory as the root for scanning
    repo_root = os.path.dirname(os.path.abspath(__file__))
    index_md_path = os.path.join(repo_root, "INDEX.md")

    print("Finding all markdown files...")
    files = find_markdown_files(repo_root)
    
    print("Updating 'Back to Main Index' links in all markdown files...")
    update_navigation_in_bulk(files, index_md_path)
    print("Back links updated.")

    if os.path.isfile(index_md_path):
        print("Generating new accordion navigation for INDEX.md...")
        nav_section = generate_accordion_navigation(CURATED_INDEX_WITH_DESC, files, index_md_path)
        
        print("Updating INDEX.md with the new navigation...")
        update_index_md_with_markers(index_md_path, nav_section)
        print("INDEX.md has been updated.")
    else:
        print(f"[Error] Main INDEX.md not found at {index_md_path}.")

    print("Process complete.")