#!/usr/bin/env python3
"""
Documentation Analysis Tool

Analyzes documentation graph to identify:
- Hub documents (highly connected)
- Low-value documents (low connectivity, redundant)
- Consolidation opportunities
"""

import json
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent


def analyze_documentation_graph() -> dict:
    """Analyze documentation graph and return insights."""
    graph_file = PROJECT_ROOT / 'docs' / 'documentation_graph.json'
    graph = json.loads(graph_file.read_text())

    # Count connections per node
    connections = defaultdict(int)
    for edge in graph.get('edges', []):
        connections[edge['source']] += 1
        connections[edge['target']] += 1

    # Categorize nodes
    nodes_by_category = defaultdict(list)
    nodes_by_connections = defaultdict(list)

    for node in graph.get('nodes', []):
        category = node.get('category', 'other')
        node_id = node['id']
        conn_count = connections.get(node_id, 0)
        nodes_by_category[category].append(node_id)
        nodes_by_connections[conn_count].append(node_id)

    # Find hub documents (top 10%)
    sorted_docs = sorted(connections.items(), key=lambda x: x[1], reverse=True)
    hub_threshold = max(1, len(sorted_docs) // 10)
    hub_docs = sorted_docs[:hub_threshold]

    # Find low-value documents (≤2 connections, not root/system/data)
    low_value = []
    for doc, count in connections.items():
        if count <= 2:
            category = next(
                (n.get('category') for n in graph.get('nodes', []) if n['id'] == doc),
                'other'
            )
            if category not in ['root', 'system', 'data']:
                low_value.append((doc, count, category))

    return {
        'total_docs': len(graph.get('nodes', [])),
        'total_connections': len(graph.get('edges', [])),
        'hub_docs': hub_docs,
        'low_value_docs': low_value,
        'by_category': dict(nodes_by_category),
        'by_connections': dict(nodes_by_connections)
    }


def main():
    """Main function."""
    analysis = analyze_documentation_graph()

    print("Documentation Analysis")
    print("=" * 60)
    print(f"Total documents: {analysis['total_docs']}")
    print(f"Total connections: {analysis['total_connections']}")
    print(f"\nHub documents (top 10%):")
    for doc, count in analysis['hub_docs'][:15]:
        print(f"  {count:3d} connections: {doc}")

    print(f"\nLow-value documents (≤2 connections, non-core):")
    for doc, count, cat in sorted(analysis['low_value_docs'], key=lambda x: x[1])[:20]:
        print(f"  {count} connections ({cat}): {doc}")

    print(f"\nDocuments by category:")
    for cat, docs in sorted(analysis['by_category'].items()):
        print(f"  {cat}: {len(docs)} documents")


if __name__ == '__main__':
    main()
