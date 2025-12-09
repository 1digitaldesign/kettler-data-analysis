#!/usr/bin/env python3
"""
Path Utilities for Python Scripts
Provides consistent path management across the project
"""

from pathlib import Path
import os

# Find project root
def find_project_root():
    """Find the project root directory"""
    current = Path(__file__).resolve()

    # Go up from scripts/utils/
    for parent in [current.parent.parent.parent, current.parent.parent]:
        readme = parent / "README.md"
        bin_dir = parent / "bin"
        if readme.exists() and bin_dir.exists():
            return parent

    # Fallback: search from current directory
    current_dir = Path.cwd()
    for _ in range(10):
        readme = current_dir / "README.md"
        bin_dir = current_dir / "bin"
        if readme.exists() and bin_dir.exists():
            return current_dir
        if current_dir == current_dir.parent:
            break
        current_dir = current_dir.parent

    # Final fallback
    return Path.cwd()

# Set project root
PROJECT_ROOT = find_project_root()

# Directory paths
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

# Research subdirectories
RESEARCH_CONNECTIONS_DIR = RESEARCH_DIR / "connections"
RESEARCH_VIOLATIONS_DIR = RESEARCH_DIR / "violations"
RESEARCH_ANOMALIES_DIR = RESEARCH_DIR / "anomalies"
RESEARCH_EVIDENCE_DIR = RESEARCH_DIR / "evidence"
RESEARCH_VERIFICATION_DIR = RESEARCH_DIR / "verification"
RESEARCH_TIMELINES_DIR = RESEARCH_DIR / "timelines"
RESEARCH_SUMMARIES_DIR = RESEARCH_DIR / "summaries"
RESEARCH_SEARCH_RESULTS_DIR = RESEARCH_DIR / "search_results"

# Ensure directories exist
def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        DATA_DIR, DATA_SOURCE_DIR, DATA_RAW_DIR, DATA_CLEANED_DIR,
        DATA_SCRAPED_DIR, DATA_VECTORS_DIR,
        RESEARCH_DIR, RESEARCH_CONNECTIONS_DIR, RESEARCH_VIOLATIONS_DIR,
        RESEARCH_ANOMALIES_DIR, RESEARCH_EVIDENCE_DIR, RESEARCH_VERIFICATION_DIR,
        RESEARCH_TIMELINES_DIR, RESEARCH_SUMMARIES_DIR, RESEARCH_SEARCH_RESULTS_DIR,
        OUTPUTS_DIR, FILINGS_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories on import
ensure_directories()
