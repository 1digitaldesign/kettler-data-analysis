#!/usr/bin/env python3
"""
Run All Unified Modules
Single entry point that replaces all R scripts
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.core import (
    UnifiedAnalyzer, UnifiedSearcher, UnifiedValidator,
    UnifiedReporter, UnifiedInvestigator, UnifiedScraper
)

def main():
    """Run all unified modules"""
    print("=" * 60)
    print("Running All Unified Modules")
    print("=" * 60)
    print()

    # Run extraction (already exists)
    print("Step 1: Extraction (use scripts/extraction/extract_all_evidence.py)")
    print("  Skipping - run separately if needed")
    print()

    # Run search
    print("Step 2: Running unified search...")
    searcher = UnifiedSearcher()
    agencies = searcher.search_regulatory_agencies()
    searcher.save_results(agencies, "regulatory_agencies_registry")
    print("  ✓ Search complete\n")

    # Run validation
    print("Step 3: Running unified validation...")
    validator = UnifiedValidator()
    validator.validate_all()
    validator.save_results()
    print("  ✓ Validation complete\n")

    # Run analysis
    print("Step 4: Running unified analysis...")
    analyzer = UnifiedAnalyzer()
    analyzer.run_all_analyses()
    analyzer.save_results()
    print("  ✓ Analysis complete\n")

    # Run investigation
    print("Step 5: Running unified investigation...")
    investigator = UnifiedInvestigator()
    investigator.run_all_investigations()
    investigator.save_results()
    print("  ✓ Investigation complete\n")

    # Run reporting
    print("Step 6: Running unified reporting...")
    reporter = UnifiedReporter()
    reporter.save_all_reports()
    print("  ✓ Reporting complete\n")

    # Run scraping (optional)
    print("Step 7: Running unified scraping...")
    scraper = UnifiedScraper()
    airbnb_results = scraper.scrape_airbnb(["800 John Carlyle", "850 John Carlyle"])
    scraper.save_results(airbnb_results, "airbnb_listings_john_carlyle.json")
    print("  ✓ Scraping complete\n")

    print("=" * 60)
    print("All Modules Complete!")
    print("=" * 60)
    print("\nAll R scripts have been replaced with unified Python modules.")
    print("See CONSOLIDATION_PLAN.md for details.")

if __name__ == "__main__":
    main()
