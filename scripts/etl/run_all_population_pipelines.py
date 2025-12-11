#!/usr/bin/env python3
"""
Run All Population Pipelines

Executes all data population pipelines in sequence for maximum efficiency.
Optimized for ARM M4 MAX with 128GB RAM.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR


def run_all_pipelines():
    """Run all population pipelines in sequence."""
    print("=" * 80)
    print("RUNNING ALL POPULATION PIPELINES")
    print("=" * 80)
    print(f"Start time: {datetime.now().isoformat()}")
    print()

    pipelines = [
        {
            "name": "Data Cleaning and Population",
            "script": "scripts/etl/data_cleaning_and_population.py",
            "description": "Initial cleaning and field population"
        },
        {
            "name": "Enhanced Population",
            "script": "scripts/etl/enhanced_data_population.py",
            "description": "Cross-reference population"
        },
        {
            "name": "MCP Browser Population",
            "script": "scripts/etl/mcp_browser_population.py",
            "description": "Ultra-parallel field mapping"
        },
        {
            "name": "Execute Browser Population",
            "script": "scripts/etl/execute_browser_population_mcp.py",
            "description": "Final execution with all records"
        }
    ]

    results = {}

    for pipeline in pipelines:
        print(f"\n{'=' * 80}")
        print(f"Running: {pipeline['name']}")
        print(f"{'=' * 80}")
        print(f"Description: {pipeline['description']}")
        print()

        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, pipeline["script"]],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per pipeline
            )

            results[pipeline["name"]] = {
                "success": result.returncode == 0,
                "stdout": result.stdout[-500:] if result.stdout else "",  # Last 500 chars
                "stderr": result.stderr[-500:] if result.stderr else "",
                "returncode": result.returncode
            }

            if result.returncode == 0:
                print(f"✓ {pipeline['name']} completed successfully")
            else:
                print(f"✗ {pipeline['name']} failed with return code {result.returncode}")

        except subprocess.TimeoutExpired:
            results[pipeline["name"]] = {
                "success": False,
                "error": "Timeout after 5 minutes"
            }
            print(f"✗ {pipeline['name']} timed out")

        except Exception as e:
            results[pipeline["name"]] = {
                "success": False,
                "error": str(e)
            }
            print(f"✗ {pipeline['name']} failed: {str(e)}")

    # Save summary
    summary_path = DATA_PROCESSED_DIR / "all_pipelines_summary.json"
    import json
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_date": datetime.now().isoformat(),
            "pipelines_run": len(pipelines),
            "pipelines_succeeded": len([r for r in results.values() if r.get("success")]),
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("ALL PIPELINES COMPLETE")
    print("=" * 80)
    print(f"  Summary: {summary_path}")
    print(f"  Pipelines succeeded: {len([r for r in results.values() if r.get('success')])}/{len(pipelines)}")
    print("=" * 80)

    return results


if __name__ == "__main__":
    run_all_pipelines()
