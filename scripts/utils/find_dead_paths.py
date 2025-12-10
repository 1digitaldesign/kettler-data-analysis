#!/usr/bin/env python3
"""
Find Dead Paths in Research Directory

Identifies:
- Empty directories
- Files not referenced anywhere
- Broken file references
- Orphaned files
"""

import os
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
RESEARCH_DIR = PROJECT_ROOT / 'research'


def find_all_files(directory: Path) -> set[str]:
    """Find all files in directory."""
    files = set()
    for f in directory.rglob('*'):
        if f.is_file():
            rel_path = str(f.relative_to(directory))
            files.add(rel_path)
            # Also add without extension
            if f.suffix:
                files.add(rel_path[:-len(f.suffix)])
    return files


def extract_file_references(directory: Path) -> set[str]:
    """Extract all file references from markdown and JSON files."""
    referenced = set()
    
    for md_file in directory.rglob('*.md'):
        try:
            content = md_file.read_text()
            # Markdown links
            links = re.findall(r'\[.*?\]\(([^)]+)\)', content)
            # Code block references
            code_refs = re.findall(r'`([^`]+\.(json|md|csv|txt))`', content)
            # Path references
            path_refs = re.findall(r'([a-zA-Z0-9_/-]+\.(json|md|csv|txt))', content)
            
            for ref in links + [c[0] for c in code_refs] + [p[0] for p in path_refs]:
                if not ref.startswith('http') and not ref.startswith('#') and ref:
                    # Normalize
                    if ref.startswith('./'):
                        ref = ref[2:]
                    if ref.startswith('../'):
                        continue  # External reference
                    referenced.add(ref)
        except Exception:
            pass
    
    # Also check JSON files for references
    for json_file in directory.rglob('*.json'):
        try:
            import json
            content = json.loads(json_file.read_text())
            # Recursively search JSON for file paths
            def find_paths(obj, paths):
                if isinstance(obj, dict):
                    for v in obj.values():
                        find_paths(v, paths)
                elif isinstance(obj, list):
                    for item in obj:
                        find_paths(item, paths)
                elif isinstance(obj, str) and ('.json' in obj or '.md' in obj):
                    if '/' in obj and not obj.startswith('http'):
                        paths.add(obj)
            
            paths = set()
            find_paths(content, paths)
            referenced.update(paths)
        except Exception:
            pass
    
    return referenced


def find_empty_directories(directory: Path) -> list[Path]:
    """Find empty directories."""
    empty = []
    for d in directory.rglob('*'):
        if d.is_dir():
            try:
                if not any(d.iterdir()):
                    empty.append(d)
            except Exception:
                pass
    return empty


def find_orphaned_files(directory: Path, referenced: set[str], actual_files: set[str]) -> list[str]:
    """Find files that are not referenced anywhere."""
    orphaned = []
    for file_path in actual_files:
        # Skip archive files
        if 'archive' in file_path:
            continue
        # Skip essential documentation
        essential = ['README.md', 'DATA_GUIDE.md', 'REPORTS.md', 'ARCHIVE.md', 
                    'QUICK_START.md', 'MASTER_INDEX.md', 'EVIDENCE_INDEX.md',
                    'COMPLAINT_AMENDMENT_GUIDE.md', 'RESEARCH_INDEX.json']
        if any(file_path.endswith(e) for e in essential):
            continue
        
        # Check if file is referenced
        found = False
        base_name = file_path
        if file_path.endswith('.md'):
            base_name = file_path[:-3]
        elif file_path.endswith('.json'):
            base_name = file_path[:-5]
        
        # Check various reference formats
        for ref in referenced:
            if (ref == file_path or ref == base_name or 
                ref.endswith(file_path) or file_path.endswith(ref) or
                ref in file_path or file_path in ref):
                found = True
                break
        
        if not found:
            orphaned.append(file_path)
    
    return orphaned


def find_broken_references(directory: Path, referenced: set[str], actual_files: set[str]) -> list[str]:
    """Find references to files that don't exist."""
    broken = []
    
    for ref in referenced:
        if ref.startswith('http') or ref.startswith('#'):
            continue
        
        # Normalize reference
        check_refs = [
            ref,
            f'{ref}.md',
            f'{ref}.json',
            ref.lstrip('./'),
        ]
        
        found = False
        for check in check_refs:
            if check in actual_files:
                found = True
                break
            # Check if file exists
            check_path = directory / check
            if check_path.exists():
                found = True
                break
        
        if not found and ref and '/' in ref:
            broken.append(ref)
    
    return broken


def main():
    """Main function."""
    print("=== Finding Dead Paths in Research Directory ===\n")
    
    # Find all files
    actual_files = find_all_files(RESEARCH_DIR)
    print(f"Total files found: {len(actual_files)}")
    
    # Find all references
    referenced = extract_file_references(RESEARCH_DIR)
    print(f"Total references found: {len(referenced)}")
    
    # Find empty directories
    empty_dirs = find_empty_directories(RESEARCH_DIR)
    print(f"\nEmpty directories: {len(empty_dirs)}")
    for d in empty_dirs:
        rel_path = d.relative_to(RESEARCH_DIR)
        print(f"  {rel_path}")
    
    # Find orphaned files
    orphaned = find_orphaned_files(RESEARCH_DIR, referenced, actual_files)
    print(f"\nOrphaned files (not referenced): {len(orphaned)}")
    for f in sorted(orphaned)[:30]:
        print(f"  {f}")
    
    # Find broken references
    broken = find_broken_references(RESEARCH_DIR, referenced, actual_files)
    print(f"\nBroken references: {len(broken)}")
    for ref in sorted(broken)[:20]:
        print(f"  {ref}")
    
    return {
        'empty_dirs': empty_dirs,
        'orphaned': orphaned,
        'broken': broken
    }


if __name__ == '__main__':
    main()
