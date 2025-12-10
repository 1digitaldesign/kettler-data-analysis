#!/usr/bin/env python3
"""
File Renaming Utility

Renames files recursively according to naming conventions.
"""

import re
from pathlib import Path
from typing import dict

PROJECT_ROOT = Path(__file__).parent.parent.parent


def screaming_snake_to_kebab(name: str) -> str:
    """Convert SCREAMING_SNAKE_CASE to kebab-case."""
    return name.lower().replace('_', '-')


def screaming_snake_to_snake(name: str) -> str:
    """Convert SCREAMING_SNAKE_CASE to snake_case."""
    return name.lower()


def create_renaming_map(directory: Path, file_type: str) -> dict[str, str]:
    """Create renaming map for files in directory."""
    renames = {}

    if file_type == 'investigations':
        # Investigation files: SCREAMING_SNAKE → kebab-case
        investigation_map = {
            'ALL_STATES_LARIAT_COMPANIES_SEARCH.md': 'lariat-companies-search.md',
            'HYLAND_UPL_EVIDENCE.md': 'hyland-upl-evidence.md',
            'KETTLER_OPERATIONAL_LOCATIONS.md': 'kettler-operational-locations.md',
            'LARIAT_AFFILIATED_COMPANIES_INVESTIGATION.md': 'lariat-affiliated-companies-investigation.md',
            'LARIAT_AFFILIATED_COMPANIES_SUMMARY.md': 'lariat-affiliated-companies-summary.md',
            'LARIAT_COMPANIES_FINDINGS.md': 'lariat-companies-findings.md',
            'LARIAT_REALTY_ADVISORS_BROKER_FOR_RENT_ANALYSIS.md': 'lariat-broker-for-rent-analysis.md',
            'LARIAT_VS_KETTLER_LICENSING_STRATEGY.md': 'lariat-vs-kettler-licensing-strategy.md',
            'METHOD_COMPARISON.md': 'method-comparison.md',
            'MOORE_KRISTEN_JONES_INVESTIGATION.md': 'moore-kristen-jones-investigation.md',
            'REMAINING_LEGAL_VIOLATIONS.md': 'remaining-legal-violations.md',
            'VIRGINIA_40_LICENSES_CRITICAL_FINDING.md': 'virginia-40-licenses-finding.md',
            'VIRGINIA_COMPANIES_FOUND.md': 'virginia-companies-found.md',
        }

        inv_dir = directory / 'investigations'
        if inv_dir.exists():
            for old_name, new_name in investigation_map.items():
                old_path = inv_dir / old_name
                if old_path.exists():
                    renames[str(old_path.relative_to(directory))] = f'investigations/{new_name}'

    elif file_type == 'json':
        # JSON files: SCREAMING_SNAKE → snake_case
        json_map = {
            'COMPLAINT_EVIDENCE_COMPILATION.json': 'complaint_evidence_compilation.json',
            'COMPLETE_RESEARCH_INVENTORY.json': 'complete_research_inventory.json',
            'RESEARCH_INDEX.json': 'research_index.json',
        }

        for old_name, new_name in json_map.items():
            old_path = directory / old_name
            if old_path.exists():
                renames[old_name] = new_name

    return renames


def update_file_references(directory: Path, renames: dict[str, str]) -> int:
    """Update file references in markdown and JSON files."""
    updated_count = 0

    for md_file in directory.rglob('*.md'):
        try:
            content = md_file.read_text()
            original_content = content

            for old_name, new_name in renames.items():
                # Update markdown links
                content = content.replace(f'({old_name})', f'({new_name})')
                content = content.replace(f'`{old_name}`', f'`{new_name}`')
                # Update without extension
                old_base = Path(old_name).stem
                new_base = Path(new_name).stem
                content = content.replace(f'({old_base})', f'({new_base})')
                content = content.replace(f'`{old_base}`', f'`{new_base}`')

            if content != original_content:
                md_file.write_text(content)
                updated_count += 1
        except Exception:
            pass

    return updated_count


def main():
    """Main function."""
    research_dir = PROJECT_ROOT / 'research'

    print("=== File Renaming Plan ===\n")

    # Create renaming maps
    investigation_renames = create_renaming_map(research_dir, 'investigations')
    json_renames = create_renaming_map(research_dir, 'json')

    print(f"Investigation files to rename: {len(investigation_renames)}")
    for old, new in sorted(investigation_renames.items()):
        print(f"  {old} → {new}")

    print(f"\nJSON files to rename: {len(json_renames)}")
    for old, new in sorted(json_renames.items()):
        print(f"  {old} → {new}")

    return {
        'investigations': investigation_renames,
        'json': json_renames
    }


if __name__ == '__main__':
    main()
