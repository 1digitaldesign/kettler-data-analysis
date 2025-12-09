#!/usr/bin/env python3
"""
List all available MCP tools
"""

import json
from pathlib import Path

def main():
    tools_file = Path(__file__).parent.parent.parent / 'mcp' / 'tools_list.json'

    with open(tools_file, 'r') as f:
        data = json.load(f)

    print("=== Available MCP Tools ===")
    print(f"\nTotal Servers: {data['metadata']['total_servers']}")
    print(f"Total Tools: {data['metadata']['total_tools']}\n")

    for server_name, server_info in data['mcp_tools'].items():
        print(f"\n[{server_name}] {server_info['description']}")
        print(f"  Server: {server_info['server']}")
        print(f"  Tools ({len(server_info['tools'])}):")
        for tool in server_info['tools']:
            print(f"    - {tool['name']}: {tool['description']}")
            if 'category' in tool:
                print(f"      Category: {tool['category']}")
            if 'parameters' in tool:
                print(f"      Parameters: {tool['parameters']}")

if __name__ == '__main__':
    main()
