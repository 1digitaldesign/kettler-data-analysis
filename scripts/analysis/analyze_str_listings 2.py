#!/usr/bin/env python3
"""
Analyze all scraped STR listings: consolidate, identify units, count violations, match with building
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import DATA_SCRAPED_DIR, RESEARCH_DIR, RESEARCH_EVIDENCE_DIR

def analyze_str_listings():
    """Analyze STR listings"""
    print("=== STR Listings Analysis ===")
    print(f"Date: {datetime.now().date()}\n")

    # Load all scraped listings
    listing_files = [
        "airbnb_listings_john_carlyle.json",
        "vrbo_listings_john_carlyle.json",
        "front_website_listings.json",
        "additional_str_listings.json"
    ]

    all_listings = {}
    for filename in listing_files:
        file_path = DATA_SCRAPED_DIR / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                all_listings[filename] = json.load(f)

    results = {
        'metadata': {
            'date': datetime.now().date().isoformat(),
            'platforms_analyzed': len(all_listings),
            'status': 'framework'
        },
        'consolidated_listings': [],
        'unit_identification': {
            'total_listings': 0,
            'unique_units': [],
            'note': 'Framework - requires listing data to analyze'
        },
        'violations': {
            'unregistered_strs': 0,
            'note': 'Framework - requires listing data to count violations'
        },
        'building_match': {
            'matched_to_800_carlyle': 0,
            'matched_to_850_carlyle': 0,
            'note': 'Framework - requires listing data to match'
        }
    }

    RESEARCH_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESEARCH_EVIDENCE_DIR / "str_listings_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Saved results to: {output_file}")

    return results

if __name__ == "__main__":
    analyze_str_listings()
