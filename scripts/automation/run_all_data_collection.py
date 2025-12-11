#!/usr/bin/env python3
"""
Run All Data Collection Tasks

Runs all data collection automation scripts in sequence.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / 'scripts' / 'automation'

SCRIPTS = [
    'run_company_registration_searches.py',
    'run_property_contract_collection.py',
    'run_regulatory_complaint_searches.py',
    'run_financial_records_searches.py',
    'run_news_coverage_searches.py',
    'run_fair_housing_searches.py',
    'run_professional_memberships_searches.py',
    'run_social_media_searches.py',
]

def run_script(script_name: str):
    """Run a data collection script."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"⚠️  Script not found: {script_name}")
        return False

    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=False
        )
        print(f"\n✓ Completed: {script_name}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}: {e}\n")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("Data Collection Automation - All Tasks")
    print("=" * 60)
    print(f"\nRunning {len(SCRIPTS)} data collection scripts...\n")

    results = []
    for script in SCRIPTS:
        success = run_script(script)
        results.append((script, success))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful

    print(f"\n✅ Successful: {successful}/{len(SCRIPTS)}")
    print(f"❌ Failed: {failed}/{len(SCRIPTS)}\n")

    if failed > 0:
        print("Failed scripts:")
        for script, success in results:
            if not success:
                print(f"  • {script}")

    print("\n✓ Data collection automation complete")
    print("\nNote: Progress dashboard updates automatically at:")
    print("  outputs/reports/progress_dashboard.html")

if __name__ == '__main__':
    main()
