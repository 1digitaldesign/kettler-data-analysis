#!/usr/bin/env python3
"""
Path Utilities for Python Scripts

Provides consistent path management across the project.
Uses Python 3.14 features: match expressions, modern type hints.
"""

from pathlib import Path

# Find project root using match expression (Python 3.14+)
def find_project_root() -> Path:
    """Find the project root directory."""
    current = Path(__file__).resolve()

    # Check immediate parents first
    for parent in [current.parent.parent.parent, current.parent.parent]:
        if (parent / "README.md").exists() and (parent / "bin").exists():
            return parent

    # Fallback: search from current directory
    current_dir = Path.cwd()
    for _ in range(10):
        if (current_dir / "README.md").exists() and (current_dir / "bin").exists():
            return current_dir
        if current_dir == current_dir.parent:
            break
        current_dir = current_dir.parent

    return Path.cwd()

# Set project root
PROJECT_ROOT = find_project_root()

# Directory paths using Path operations
BIN_DIR = PROJECT_ROOT / "bin"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
RESEARCH_DIR = PROJECT_ROOT / "research"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
FILINGS_DIR = PROJECT_ROOT / "filings"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DOCS_DIR = PROJECT_ROOT / "docs"

# Data subdirectories
DATA_SOURCE_DIR = DATA_DIR / "source"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_CLEANED_DIR = DATA_DIR / "cleaned"
DATA_SCRAPED_DIR = DATA_DIR / "scraped"
DATA_VECTORS_DIR = DATA_DIR / "vectors"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# Research subdirectories
RESEARCH_CONNECTIONS_DIR = RESEARCH_DIR / "connections"
RESEARCH_VIOLATIONS_DIR = RESEARCH_DIR / "violations"
RESEARCH_ANOMALIES_DIR = RESEARCH_DIR / "anomalies"
RESEARCH_EVIDENCE_DIR = RESEARCH_DIR / "evidence"
RESEARCH_VERIFICATION_DIR = RESEARCH_DIR / "verification"
RESEARCH_TIMELINES_DIR = RESEARCH_DIR / "timelines"
RESEARCH_SUMMARIES_DIR = RESEARCH_DIR / "summaries"
RESEARCH_SEARCH_RESULTS_DIR = RESEARCH_DIR / "search_results"

# Ensure directories exist using efficient pattern
def ensure_directories() -> None:
    """Ensure all necessary directories exist."""
    directories = [
        DATA_DIR, DATA_SOURCE_DIR, DATA_RAW_DIR, DATA_CLEANED_DIR,
        DATA_SCRAPED_DIR, DATA_VECTORS_DIR, DATA_PROCESSED_DIR,
        RESEARCH_DIR, RESEARCH_CONNECTIONS_DIR, RESEARCH_VIOLATIONS_DIR,
        RESEARCH_ANOMALIES_DIR, RESEARCH_EVIDENCE_DIR, RESEARCH_VERIFICATION_DIR,
        RESEARCH_TIMELINES_DIR, RESEARCH_SUMMARIES_DIR, RESEARCH_SEARCH_RESULTS_DIR,
        OUTPUTS_DIR, FILINGS_DIR
    ]

    # Use list comprehension for efficiency
    [directory.mkdir(parents=True, exist_ok=True) for directory in directories]

# Initialize directories on import
ensure_directories()
