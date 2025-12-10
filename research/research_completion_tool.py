#!/usr/bin/env python3
"""
Research Completion Tool

Scans research JSON files, identifies incomplete ones, and provides tools
to complete them using browser automation and web searches.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

class ResearchCompleter:
    def __init__(self, research_dir: Path):
        self.research_dir = research_dir
        self.incomplete_files = []
        self.completion_tasks = []

    def scan_json_files(self) -> List[Dict[str, Any]]:
        """Scan all JSON files and identify incomplete ones."""
        incomplete = []

        for json_file in self.research_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                status = self.check_completion_status(data, json_file)
                if not status['complete']:
                    incomplete.append({
                        'file': str(json_file.relative_to(self.research_dir)),
                        'status': status,
                        'data': data
                    })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

        return incomplete

    def check_completion_status(self, data: Any, file_path: Path) -> Dict[str, Any]:
        """Check if a JSON file is complete."""
        status = {
            'complete': True,
            'issues': [],
            'pending_fields': [],
            'incomplete_sections': []
        }

        if isinstance(data, dict):
            # Check for status fields
            if 'status' in data:
                status_val = data['status']
                if status_val in ['pending', 'in_progress', 'partial']:
                    status['complete'] = False
                    status['issues'].append(f"Status: {status_val}")

            # Check for data_collection_status
            if 'data_collection_status' in data:
                if data['data_collection_status'] in ['pending', 'in_progress']:
                    status['complete'] = False
                    status['issues'].append(f"Data collection: {data['data_collection_status']}")

            # Check for empty findings arrays
            if 'findings' in data:
                if isinstance(data['findings'], list) and len(data['findings']) == 0:
                    status['complete'] = False
                    status['issues'].append("Empty findings array")

            # Check for pending sections
            for key, value in data.items():
                if isinstance(value, dict):
                    if 'status' in value and value['status'] in ['pending', 'in_progress', 'partial']:
                        status['complete'] = False
                        status['incomplete_sections'].append(key)

                # Check for "unknown" or empty string values
                if isinstance(value, str) and value.lower() in ['unknown', 'pending', 'tbd', '']:
                    status['complete'] = False
                    status['pending_fields'].append(key)

        return status

    def generate_todos(self, incomplete_files: List[Dict]) -> List[Dict[str, Any]]:
        """Generate todos for completing research files."""
        todos = []

        for file_info in incomplete_files:
            file_path = file_info['file']
            status = file_info['status']
            data = file_info['data']

            # Generate specific todos based on file type and issues
            if 'va_dpor_complaint' in file_path:
                todos.extend(self._generate_complaint_todos(file_path, data, status))
            elif 'verification' in file_path:
                todos.extend(self._generate_verification_todos(file_path, data, status))
            elif 'connections' in file_path:
                todos.extend(self._generate_connection_todos(file_path, data, status))
            else:
                # Generic todo
                todos.append({
                    'id': f"complete-{Path(file_path).stem}",
                    'file': file_path,
                    'description': f"Complete research in {file_path}",
                    'issues': status['issues'],
                    'priority': 'medium'
                })

        return todos

    def _generate_complaint_todos(self, file_path: str, data: Dict, status: Dict) -> List[Dict]:
        """Generate todos for complaint research files."""
        todos = []
        file_stem = Path(file_path).stem

        if 'principal_broker_gap' in file_stem:
            if 'historical_principal_broker_search' in data:
                search = data['historical_principal_broker_search']
                if search.get('status') == 'in_progress':
                    todos.append({
                        'id': f"wayback-dpor-{file_stem}",
                        'file': file_path,
                        'description': 'Search Wayback Machine for DPOR historical records',
                        'method': 'browser',
                        'url': 'https://web.archive.org',
                        'priority': 'high'
                    })

        if 'operations_gap' in file_stem:
            if data.get('data_collection_status') == 'in_progress':
                todos.append({
                    'id': f"property-records-{file_stem}",
                    'file': file_path,
                    'description': 'Search property records for unit counts',
                    'method': 'browser',
                    'priority': 'high'
                })

        if 'regulatory_compliance' in file_stem:
            if 'regulatory_issues' in data:
                issues = data['regulatory_issues']
                for key, value in issues.items():
                    if isinstance(value, dict) and value.get('status') == 'pending':
                        todos.append({
                            'id': f"regulatory-{key}-{file_stem}",
                            'file': file_path,
                            'description': f"Research {key} regulatory issues",
                            'method': 'browser',
                            'priority': 'medium'
                        })

        return todos

    def _generate_verification_todos(self, file_path: str, data: Dict, status: Dict) -> List[Dict]:
        """Generate todos for verification files."""
        todos = []
        file_stem = Path(file_path).stem

        if 'personnel' in file_stem or 'license' in file_stem:
            if 'personnel_list' in data:
                for person in data['personnel_list']:
                    if 'license_verification' in person:
                        for state, verification in person['license_verification'].items():
                            if verification.get('status') == 'pending':
                                todos.append({
                                    'id': f"verify-{person['name'].lower().replace(' ', '-')}-{state}",
                                    'file': file_path,
                                    'description': f"Verify {person['name']} license in {state}",
                                    'method': 'browser',
                                    'priority': 'high'
                                })

        return todos

    def _generate_connection_todos(self, file_path: str, data: Dict, status: Dict) -> List[Dict]:
        """Generate todos for connection analysis files."""
        todos = []
        # Add connection-specific todos
        return todos

    def print_report(self, incomplete_files: List[Dict], todos: List[Dict]):
        """Print completion report."""
        print("=" * 70)
        print("RESEARCH COMPLETION REPORT")
        print("=" * 70)
        print(f"\nIncomplete Files: {len(incomplete_files)}")
        print(f"Generated Todos: {len(todos)}\n")

        print("\nIncomplete Files:")
        for file_info in incomplete_files:
            print(f"  - {file_info['file']}")
            for issue in file_info['status']['issues']:
                print(f"    ⚠️  {issue}")

        print("\nGenerated Todos:")
        for todo in todos:
            print(f"  - [{todo['priority'].upper()}] {todo['id']}: {todo['description']}")


def main():
    """Run research completion scan."""
    research_dir = Path(__file__).parent
    completer = ResearchCompleter(research_dir)

    incomplete = completer.scan_json_files()
    todos = completer.generate_todos(incomplete)

    completer.print_report(incomplete, todos)

    # Save todos to JSON
    todos_file = research_dir / "research_completion_todos.json"
    with open(todos_file, 'w') as f:
        json.dump({
            'scan_date': str(Path(__file__).stat().st_mtime),
            'incomplete_files': len(incomplete),
            'todos': todos
        }, f, indent=2)

    print(f"\n✅ Todos saved to {todos_file}")


if __name__ == "__main__":
    main()
