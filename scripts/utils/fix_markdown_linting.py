#!/usr/bin/env python3
"""
Markdown Linting Fixer

Fixes common markdown linting issues:
- Trailing whitespace
- Lines with only whitespace
- Missing blank lines between sections
- Inconsistent formatting

Uses Python 3.14 features.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent.parent


def fix_trailing_whitespace(content: str) -> str:
    """Remove trailing whitespace from all lines."""
    lines = content.split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def fix_blank_lines(content: str) -> str:
    """Ensure proper blank lines between sections."""
    lines = content.split('\n')
    fixed_lines = []
    prev_line_empty = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        is_empty = not stripped

        # Skip multiple consecutive empty lines (keep max 2)
        if is_empty and prev_line_empty and fixed_lines and fixed_lines[-1].strip() == '':
            continue

        # Ensure blank line before headers (except first line)
        if stripped.startswith('#') and fixed_lines and fixed_lines[-1].strip() != '':
            # Check if previous line is already empty
            if fixed_lines[-1].strip() != '':
                fixed_lines.append('')

        fixed_lines.append(line.rstrip())
        prev_line_empty = is_empty

    return '\n'.join(fixed_lines)


def fix_line_endings(content: str) -> str:
    """Ensure consistent line endings."""
    # Remove trailing newlines, then add one at the end
    content = content.rstrip('\n\r')
    return content + '\n'


def fix_markdown_file(file_path: Path) -> tuple[bool, int]:
    """
    Fix markdown linting issues in a file.

    Returns:
        tuple[bool, int]: (file_was_modified, number_of_fixes)
    """
    try:
        original_content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return False, 0

    fixes = 0
    content = original_content

    # Fix trailing whitespace
    new_content = fix_trailing_whitespace(content)
    if new_content != content:
        fixes += 1
        content = new_content

    # Fix blank lines
    new_content = fix_blank_lines(content)
    if new_content != content:
        fixes += 1
        content = new_content

    # Fix line endings
    new_content = fix_line_endings(content)
    if new_content != content:
        fixes += 1
        content = new_content

    # Write back if changed
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True, fixes

    return False, 0


def find_markdown_files() -> list[Path]:
    """Find all markdown files in the repository."""
    md_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip hidden directories, venv, node_modules
        dirs[:] = [
            d for d in dirs
            if not d.startswith('.')
            and d != 'node_modules'
            and not d.startswith('venv')
            and 'venv' not in str(Path(root) / d)
        ]
        root_path = Path(root)
        if 'venv' not in str(root_path):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(root_path / file)
    return sorted(md_files)


def main() -> int:
    """Main function."""
    md_files = find_markdown_files()
    total_fixed = 0
    files_modified = 0

    print(f"Checking {len(md_files)} markdown files...")

    for md_file in md_files:
        modified, fixes = fix_markdown_file(md_file)
        if modified:
            files_modified += 1
            total_fixed += fixes
            rel_path = md_file.relative_to(PROJECT_ROOT)
            print(f"Fixed {rel_path} ({fixes} issue(s))")

    print(f"\n✅ Fixed {total_fixed} issue(s) in {files_modified} file(s)")
    return 0 if total_fixed == 0 else 0  # Always return 0 (success)


if __name__ == '__main__':
    sys.exit(main())
