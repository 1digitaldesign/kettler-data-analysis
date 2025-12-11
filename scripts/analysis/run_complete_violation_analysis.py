#!/usr/bin/env python3
"""
Master script to run complete violation analysis pipeline
Orchestrates all analysis steps in proper order
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, RESEARCH_DIR


def run_script(script_path: Path, description: str) -> bool:
    """Run a Python script and return success status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            capture_output=False,
            text=True
        )

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False


def main():
    """Run complete violation analysis pipeline"""
    print("=" * 60)
    print("Complete Violation Analysis Pipeline")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    scripts_dir = PROJECT_ROOT / "scripts" / "analysis"

    # Step 1: Preprocess data
    print("\n" + "="*60)
    print("STEP 1: Data Preprocessing")
    print("="*60)
    success = run_script(
        scripts_dir / "preprocess_violation_data.py",
        "Data preprocessing and enrichment"
    )
    if not success:
        print("\n⚠ Warning: Preprocessing had issues, but continuing...")

    # Step 2: Extract violations
    print("\n" + "="*60)
    print("STEP 2: Violation Extraction")
    print("="*60)
    success = run_script(
        scripts_dir / "enhanced_violation_extraction.py",
        "Enhanced violation extraction"
    )
    if not success:
        print("\n⚠ Warning: Violation extraction had issues, but continuing...")

    # Step 3: Embedding analysis
    print("\n" + "="*60)
    print("STEP 3: Embedding-Based Analysis")
    print("="*60)
    success = run_script(
        scripts_dir / "embedding_violation_analysis.py",
        "Embedding similarity analysis"
    )
    if not success:
        print("\n⚠ Warning: Embedding analysis had issues, but continuing...")

    # Step 4: Cross-reference
    print("\n" + "="*60)
    print("STEP 4: Cross-Reference Analysis")
    print("="*60)
    success = run_script(
        scripts_dir / "cross_reference_violations.py",
        "Cross-reference with research data"
    )
    if not success:
        print("\n⚠ Warning: Cross-reference had issues, but continuing...")

    # Step 5: ML Analysis
    print("\n" + "="*60)
    print("STEP 5: ML-Based Analysis")
    print("="*60)
    success = run_script(
        scripts_dir / "ml_tax_structure_analysis.py",
        "ML tax structure analysis"
    )
    if not success:
        print("\n⚠ Warning: ML analysis had issues, but continuing...")

    # Step 6: Generate comprehensive report
    print("\n" + "="*60)
    print("STEP 6: Report Generation")
    print("="*60)
    success = run_script(
        scripts_dir / "generate_ml_violation_report.py",
        "ML-enhanced violation report generation"
    )
    if not success:
        print("\n⚠ Warning: Report generation had issues")

    # Step 7: Enhanced existing analysis (optional)
    print("\n" + "="*60)
    print("STEP 7: Enhanced Tax Hub Analysis")
    print("="*60)
    success = run_script(
        scripts_dir / "analyze_tax_hub_violations.py",
        "Enhanced tax hub violations analysis"
    )
    if not success:
        print("\n⚠ Warning: Enhanced analysis had issues")

    # Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check output files
    print("\nGenerated Files:")
    output_files = [
        (DATA_PROCESSED_DIR / "lariat_enriched.json", "Enriched entities"),
        (DATA_PROCESSED_DIR / "extracted_violations.json", "Extracted violations"),
        (DATA_PROCESSED_DIR / "embedding_similarity_analysis.json", "Embedding analysis"),
        (DATA_PROCESSED_DIR / "cross_referenced_violations.json", "Cross-referenced data"),
        (DATA_PROCESSED_DIR / "ml_tax_structure_analysis.json", "ML analysis"),
        (RESEARCH_DIR / "texas" / "analysis" / "ml_comprehensive_violations_analysis.json", "Comprehensive report"),
        (RESEARCH_DIR / "texas" / "analysis" / "ml_violations_summary.md", "Markdown summary")
    ]

    for file_path, description in output_files:
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {description}: {file_path} ({size:,} bytes)")
        else:
            print(f"  ✗ {description}: {file_path} (not found)")

    print("\n" + "="*60)
    print("Analysis pipeline finished!")
    print("="*60)


if __name__ == '__main__':
    main()
