#!/usr/bin/env python3
"""
ML Pipeline Runner for Law Ground Truth Integration
Runs the complete ML pipeline: law references, violations integration, and analysis
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR, DATA_RAW_DIR
from scripts.analysis.law_ground_truth_integration import LawGroundTruthSystem
from scripts.utils.create_law_references import main as create_law_references


def run_complete_pipeline():
    """Run the complete ML pipeline"""
    print("=" * 80)
    print("ML Pipeline: Law Ground Truth Integration")
    print("=" * 80)
    print()

    # Step 1: Skip if law references already exist (to save time)
    print("Step 1: Checking Law References...")
    print("-" * 80)
    law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    if law_file.exists():
        print("✅ Law references file exists, skipping creation\n")
    else:
        try:
            create_law_references()
            print("✅ Law references created/updated\n")
        except Exception as e:
            print(f"⚠️  Warning creating law references: {e}")
            print("Continuing with existing references...\n")

    # Step 2: Run integration system
    print("Step 2: Running Law Ground Truth Integration...")
    print("-" * 80)
    system = LawGroundTruthSystem()

    # Load data
    law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    violations_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    lariat_embeddings_file = DATA_VECTORS_DIR / "lariat_tx_embeddings.json"
    lariat_txt_file = DATA_RAW_DIR / "lariat.txt"

    system.load_law_references(law_file)
    system.load_violations(violations_file)
    system.load_lariat_embeddings(lariat_embeddings_file)
    system.load_lariat_txt(lariat_txt_file)

    # Process research intersections (limited for speed)
    print("\nStep 3: Processing Research Intersections (limited for performance)...")
    print("-" * 80)
    system.process_research_intersections(max_files=50)  # Limit to 50 files for speed

    # Match violations to laws
    print("\nStep 4: Matching Violations to Laws...")
    print("-" * 80)
    system.match_violations_to_laws(threshold=0.5)

    # Generate ML analysis
    print("\nStep 5: Generating ML Analysis...")
    print("-" * 80)
    ml_analysis = system.generate_ml_analysis()

    # Save results
    print("\nStep 6: Saving Results...")
    print("-" * 80)
    output_file = DATA_PROCESSED_DIR / "law_ground_truth_integration.json"
    system.save_results(output_file)

    # Print summary
    print("\n" + "=" * 80)
    print("✅ ML Pipeline Complete!")
    print("=" * 80)
    print(f"\nResults:")
    print(f"  - Output file: {output_file}")
    print(f"  - Matched violations: {len(system.matched_violations)}")
    print(f"  - Law references: {len(system.extract_law_embeddings())}")
    print(f"  - Research intersections:")
    print(f"    * Licenses: {len(system.research_intersections.get('licenses', []))}")
    print(f"    * Violations: {len(system.research_intersections.get('violations', []))}")
    print(f"    * Connections: {len(system.research_intersections.get('connections', []))}")

    if system.matched_violations:
        print(f"\nTop 5 Violation-Law Matches:")
        sorted_matches = sorted(system.matched_violations,
                               key=lambda x: x.get('similarity', 0),
                               reverse=True)[:5]
        for i, match in enumerate(sorted_matches, 1):
            violation_id = match['violation'].get('id', 'unknown')
            law_name = match['law'].get('name', 'unknown')
            similarity = match.get('similarity', 0)
            print(f"  {i}. {violation_id[:50]}...")
            print(f"     → {law_name[:60]}...")
            print(f"     Similarity: {similarity:.3f}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    run_complete_pipeline()
