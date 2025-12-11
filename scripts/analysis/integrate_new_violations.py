#!/usr/bin/env python3
"""
Integrate Newly Discovered Violations with Law Ground Truth System
Merges new violations with existing ones and matches to laws
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR
from scripts.analysis.law_ground_truth_integration import LawGroundTruthSystem


def merge_violations(existing_file: Path, new_file: Path, output_file: Path):
    """Merge existing and newly discovered violations"""
    print("=" * 80)
    print("🔄 Integrating New Violations with Existing Dataset")
    print("=" * 80)
    print()

    # Load existing violations
    print("Loading existing violations...")
    with open(existing_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    existing_violations = existing_data.get("violations", {})
    print(f"✅ Loaded {sum(len(v) for v in existing_violations.values())} existing violations")

    # Load new violations
    print("\nLoading newly discovered violations...")
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)

    new_violations = new_data.get("violations", {})
    print(f"✅ Loaded {sum(len(v) for v in new_violations.values())} new violations")

    # Merge violations by category
    print("\nMerging violations...")
    merged = {}
    total_existing = 0
    total_new = 0

    # Get all categories
    all_categories = set(existing_violations.keys()) | set(new_violations.keys())

    for category in all_categories:
        existing_items = existing_violations.get(category, [])
        new_items = new_violations.get(category, [])

        # Create unique keys to avoid duplicates
        existing_keys = set()
        for item in existing_items:
            entity = item.get("entity_name", "").lower()
            vtype = item.get("violation_type", "").lower()
            date = item.get("filing_date") or item.get("effective_date") or item.get("date", "")
            key = f"{entity}_{vtype}_{date}"
            existing_keys.add(key)

        # Add new items that aren't duplicates
        unique_new = []
        for item in new_items:
            entity = item.get("entity_name", "").lower()
            vtype = item.get("violation_type", "").lower()
            date = item.get("date") or item.get("filing_date") or item.get("effective_date", "")
            key = f"{entity}_{vtype}_{date}"

            if key not in existing_keys:
                unique_new.append(item)
                total_new += 1
            else:
                print(f"   ⚠️  Skipping duplicate: {entity} - {vtype}")

        merged[category] = existing_items + unique_new
        total_existing += len(existing_items)

    print(f"✅ Merged violations:")
    print(f"   - Existing: {total_existing}")
    print(f"   - New (unique): {total_new}")
    print(f"   - Total: {total_existing + total_new}")

    # Create merged dataset
    merged_data = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "2.0.0",
            "description": "Integrated violations dataset (existing + newly discovered)",
            "total_violations": total_existing + total_new,
            "categories": list(merged.keys()),
            "sources": {
                "existing": existing_file.name,
                "new": new_file.name
            }
        },
        "violations": merged
    }

    # Save merged dataset
    print(f"\n💾 Saving integrated violations dataset...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved to {output_file}")

    return merged_data


def match_new_violations_to_laws(merged_violations_file: Path):
    """Match newly integrated violations to ground truth laws"""
    print("\n" + "=" * 80)
    print("🔗 Matching Integrated Violations to Ground Truth Laws")
    print("=" * 80)
    print()

    system = LawGroundTruthSystem()

    # Load law references
    law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    system.load_law_references(law_file)

    # Load merged violations
    system.load_violations(merged_violations_file)

    # Match violations to laws
    system.match_violations_to_laws(threshold=0.5)

    # Generate analysis
    ml_analysis = system.generate_ml_analysis()

    # Save results
    output_file = DATA_PROCESSED_DIR / "integrated_violations_with_laws.json"
    system.save_results(output_file)

    print(f"\n✅ Matched {len(system.matched_violations)} violations to laws")
    print(f"   Results saved to: {output_file}")

    return system.matched_violations


def main():
    """Main function to integrate new violations"""
    existing_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    new_file = DATA_PROCESSED_DIR / "newly_discovered_violations.json"
    merged_file = DATA_PROCESSED_DIR / "integrated_violations.json"

    # Merge violations
    merged_data = merge_violations(existing_file, new_file, merged_file)

    # Match to laws
    matches = match_new_violations_to_laws(merged_file)

    print("\n" + "=" * 80)
    print("✅ Integration Complete!")
    print("=" * 80)
    print(f"Total violations: {merged_data['metadata']['total_violations']}")
    print(f"Matched to laws: {len(matches)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
