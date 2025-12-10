#!/usr/bin/env python3
"""
Documentation Link Checker

Checks all markdown files for broken internal links and generates a documentation graph.
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent


def find_markdown_files() -> list[Path]:
    """Find all markdown files in the repository."""
    md_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return sorted(md_files)


def extract_links(content: str, file_path: Path) -> list[tuple[str, str]]:
    """Extract all markdown links from content."""
    links = []
    # Find all markdown links [text](path)
    matches = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    for match in matches:
        link_text = match.group(1)
        link_path = match.group(2)
        links.append((link_text, link_path))
    return links


def resolve_link(link_path: str, base_file: Path) -> Tuple[bool, Path]:
    """Resolve a link path relative to base file."""
    # External links
    if link_path.startswith(('http://', 'https://')):
        return True, None

    # Anchor links
    if link_path.startswith('#'):
        return True, None

    # Remove anchor if present
    if '#' in link_path:
        link_path = link_path.split('#')[0]

    # Resolve relative to base file
    if link_path.startswith('/'):
        # Absolute from repo root
        resolved = PROJECT_ROOT / link_path.lstrip('/')
    else:
        # Relative to base file
        resolved = (base_file.parent / link_path).resolve()

    # Check if file exists
    exists = resolved.exists()
    return exists, resolved


def check_all_links() -> dict[str, list[dict]]:
    """Check all links in all markdown files."""
    md_files = find_markdown_files()
    results = {}

    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}", file=sys.stderr)
            continue

        links = extract_links(content, md_file)
        file_results = []

        for link_text, link_path in links:
            exists, resolved = resolve_link(link_path, md_file)
            file_results.append({
                'text': link_text,
                'path': link_path,
                'exists': exists,
                'resolved': str(resolved) if resolved else None
            })

        if file_results:
            results[str(md_file.relative_to(PROJECT_ROOT))] = file_results

    return results


def build_documentation_graph() -> Dict:
    """Build a graph of documentation relationships."""
    md_files = find_markdown_files()
    graph = {
        'nodes': [],
        'edges': []
    }

    # Create nodes
    for md_file in md_files:
        rel_path = str(md_file.relative_to(PROJECT_ROOT))
        graph['nodes'].append({
            'id': rel_path,
            'label': md_file.stem,
            'path': rel_path,
            'category': determine_category(rel_path)
        })

    # Create edges (links between files)
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        links = extract_links(content, md_file)
        source = str(md_file.relative_to(PROJECT_ROOT))

        for link_text, link_path in links:
            exists, resolved = resolve_link(link_path, md_file)
            if exists and resolved and resolved.suffix == '.md':
                target = str(resolved.relative_to(PROJECT_ROOT))
                if target != source:  # Avoid self-loops
                    graph['edges'].append({
                        'source': source,
                        'target': target,
                        'label': link_text
                    })

    return graph


def determine_category(file_path: str) -> str:
    """Determine category of documentation file."""
    if file_path.startswith('docs/'):
        if 'guide' in file_path.lower():
            return 'guide'
        elif 'reference' in file_path.lower():
            return 'reference'
        else:
            return 'system'
    elif file_path.startswith('data/'):
        return 'data'
    elif file_path.startswith('research/'):
        return 'research'
    elif file_path in ['README.md', 'INSTALLATION.md', 'QUICK_START.md', 'STATUS.md']:
        return 'root'
    else:
        return 'other'


def generate_mermaid_graph(graph: dict) -> str:
    """Generate Mermaid.js graph from documentation graph."""
    lines = ['graph TB']

    # Group nodes by category using defaultdict (Python 3.11+)
    from collections import defaultdict
    categories: defaultdict[str, list[dict]] = defaultdict(list)
    for node in graph['nodes']:
        categories[node['category']].append(node)

    # Create subgraphs for each category
    for cat, nodes in categories.items():
        lines.append(f'    subgraph "{cat.upper()}"')
        for node in nodes:
            node_id = node['id'].replace('/', '_').replace('.', '_').replace('-', '_')
            label = node['label'].replace(' ', '_')
            lines.append(f'        {node_id}["{label}"]')
        lines.append('    end')

    # Add edges
    for edge in graph['edges']:
        source_id = edge['source'].replace('/', '_').replace('.', '_').replace('-', '_')
        target_id = edge['target'].replace('/', '_').replace('.', '_').replace('-', '_')
        lines.append(f'    {source_id} --> {target_id}')

    # Add styling
    color_map = {
        'root': '#C8E6C9',
        'system': '#B3E5FC',
        'data': '#FFF9C4',
        'research': '#E1BEE7',
        'guide': '#F8BBD0',
        'reference': '#FFE0B2',
        'other': '#D1C4E9'
    }

    for cat, color in color_map.items():
        if cat in categories:
            for node in categories[cat]:
                node_id = node['id'].replace('/', '_').replace('.', '_').replace('-', '_')
                lines.append(f'    style {node_id} fill:{color}')

    return '\n'.join(lines)


if __name__ == '__main__':
    import os

    print("Checking documentation links...")
    results = check_all_links()

    # Count broken links
    broken = []
    for file_path, links in results.items():
        for link in links:
            if not link['exists'] and not link['path'].startswith('http'):
                broken.append((file_path, link['text'], link['path']))

    if broken:
        print(f"\n⚠️  Found {len(broken)} broken links:")
        for file_path, text, path in broken[:10]:
            print(f"  {file_path}: [{text}]({path})")
    else:
        print("✅ All internal links are valid!")

    print("\nBuilding documentation graph...")
    graph = build_documentation_graph()

    # Save graph as JSON
    graph_file = PROJECT_ROOT / 'docs' / 'documentation_graph.json'
    with open(graph_file, 'w') as f:
        json.dump(graph, f, indent=2)
    print(f"✅ Graph saved to {graph_file}")

    # Generate Mermaid diagram
    mermaid = generate_mermaid_graph(graph)
    print(f"\n✅ Generated Mermaid graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")

    # Save Mermaid diagram
    mermaid_file = PROJECT_ROOT / 'docs' / 'DOCUMENTATION_GRAPH.md'
    with open(mermaid_file, 'w') as f:
        f.write("# Documentation Graph\n\n")
        f.write("Complete graph of all documentation files and their relationships.\n\n")
        f.write("```mermaid\n")
        f.write(mermaid)
        f.write("\n```\n")
    print(f"✅ Mermaid diagram saved to {mermaid_file}")
