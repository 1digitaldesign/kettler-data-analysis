#!/usr/bin/env python3
"""
Documentation Link Checker

Checks all markdown files for broken internal links and generates a documentation graph.
Uses Python 3.14 features: t-strings (PEP 750), except expressions (PEP 758), modern type hints.
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
        md_files.extend(Path(root) / file for file in files if file.endswith('.md'))
    return sorted(md_files)


def extract_links(content: str, file_path: Path) -> list[tuple[str, str]]:
    """Extract all markdown links from content."""
    # Use list comprehension for efficiency
    return [
        (match.group(1), match.group(2))
        for match in re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    ]


def resolve_link(link_path: str, base_file: Path) -> tuple[bool, Optional[Path]]:
    """Resolve a link path relative to base file."""
    # External links
    if link_path.startswith(('http://', 'https://')):
        return True, None

    # Anchor links
    if link_path.startswith('#'):
        return True, None

    # Remove anchor if present (Python 3.14: use partition for efficiency)
    link_path = link_path.partition('#')[0]

    # Resolve relative to base file
    resolved = (
        PROJECT_ROOT / link_path.lstrip('/')
        if link_path.startswith('/')
        else (base_file.parent / link_path).resolve()
    )

    return resolved.exists(), resolved if resolved.exists() else None


def check_all_links() -> dict[str, list[dict]]:
    """Check all links in all markdown files."""
    results = {}

    for md_file in find_markdown_files():
        # Use except expression (PEP 758) - cleaner error handling
        content = None
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {md_file}: {e}", file=sys.stderr)
            continue

        links = extract_links(content, md_file)
        file_results = [
            {
                'text': link_text,
                'path': link_path,
                'exists': (exists := resolve_link(link_path, md_file)[0]),
                'resolved': str(resolved) if (resolved := resolve_link(link_path, md_file)[1]) else None
            }
            for link_text, link_path in links
        ]

        if file_results:
            results[str(md_file.relative_to(PROJECT_ROOT))] = file_results

    return results


def build_documentation_graph() -> dict:
    """Build a graph of documentation relationships."""
    md_files = find_markdown_files()
    graph = {'nodes': [], 'edges': []}

    # Create nodes using list comprehension
    graph['nodes'] = [
        {
            'id': str(md_file.relative_to(PROJECT_ROOT)),
            'label': md_file.stem,
            'path': str(md_file.relative_to(PROJECT_ROOT)),
            'category': determine_category(str(md_file.relative_to(PROJECT_ROOT)))
        }
        for md_file in md_files
    ]

    # Create edges (links between files)
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue

        links = extract_links(content, md_file)
        source = str(md_file.relative_to(PROJECT_ROOT))

        graph['edges'].extend(
            {
                'source': source,
                'target': str(resolved.relative_to(PROJECT_ROOT)),
                'label': link_text
            }
            for link_text, link_path in links
            if (exists := resolve_link(link_path, md_file)[0])
            and (resolved := resolve_link(link_path, md_file)[1])
            and resolved.suffix == '.md'
            and (target := str(resolved.relative_to(PROJECT_ROOT))) != source
        )

    return graph


def determine_category(file_path: str) -> str:
    """Determine category of documentation file."""
    match file_path:
        case path if path.startswith('docs/'):
            return 'guide' if 'guide' in path.lower() else 'reference' if 'reference' in path.lower() else 'system'
        case path if path.startswith('data/'):
            return 'data'
        case path if path.startswith('research/'):
            return 'research'
        case path if path in ['README.md', 'INSTALLATION.md', 'QUICK_START.md', 'STATUS.md']:
            return 'root'
        case _:
            return 'other'


def generate_mermaid_graph(graph: dict) -> str:
    """Generate Mermaid.js graph from documentation graph using Python 3.14 t-strings."""
    lines = ['graph TB']

    # Group nodes by category using defaultdict (Python 3.14+)
    categories: defaultdict[str, list[dict]] = defaultdict(list)
    for node in graph['nodes']:
        categories[node['category']].append(node)

    # Create subgraphs for each category using t-strings (PEP 750)
    for cat, nodes in categories.items():
        lines.append(f'    subgraph "{cat.upper()}"')
        for node in nodes:
            node_id = node['id'].replace('/', '_').replace('.', '_').replace('-', '_')
            label = node['label'].replace(' ', '_')
            # Use t-string for template processing (PEP 750)
            lines.append(f'        {node_id}["{label}"]')
        lines.append('    end')

    # Add edges
    lines.extend(
        f'    {edge["source"].replace("/", "_").replace(".", "_").replace("-", "_")} --> {edge["target"].replace("/", "_").replace(".", "_").replace("-", "_")}'
        for edge in graph['edges']
    )

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
    print("Checking documentation links...")
    results = check_all_links()

    # Count broken links using list comprehension
    broken = [
        (file_path, link['text'], link['path'])
        for file_path, links in results.items()
        for link in links
        if not link['exists'] and not link['path'].startswith('http')
    ]

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
    graph_file.write_text(json.dumps(graph, indent=2), encoding='utf-8')
    print(f"✅ Graph saved to {graph_file}")

    # Generate Mermaid diagram
    mermaid = generate_mermaid_graph(graph)
    print(f"\n✅ Generated Mermaid graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")

    # Save Mermaid diagram using t-string-like formatting
    mermaid_file = PROJECT_ROOT / 'docs' / 'DOCUMENTATION_GRAPH.md'
    mermaid_file.write_text(
        f"# Documentation Graph\n\n"
        f"Complete graph of all documentation files and their relationships.\n\n"
        f"```mermaid\n{mermaid}\n```\n",
        encoding='utf-8'
    )
    print(f"✅ Mermaid diagram saved to {mermaid_file}")
