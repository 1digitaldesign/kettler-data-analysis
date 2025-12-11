#!/usr/bin/env python3
"""
Generate Summary Report of Discovered and Curated Violations
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR


def generate_summary():
    """Generate comprehensive summary of violations"""
    print("=" * 80)
    print("📊 Violation Discovery and Curation Summary")
    print("=" * 80)
    print()

    # Load integrated violations
    integrated_file = DATA_PROCESSED_DIR / "integrated_violations.json"
    with open(integrated_file, 'r', encoding='utf-8') as f:
        integrated_data = json.load(f)

    # Load law matches
    law_matches_file = DATA_PROCESSED_DIR / "integrated_violations_with_laws.json"
    with open(law_matches_file, 'r', encoding='utf-8') as f:
        law_matches_data = json.load(f)

    violations = integrated_data.get("violations", {})
    matches = law_matches_data.get("matched_violations", [])

    print("📈 Violation Statistics:")
    print("-" * 80)
    total_violations = sum(len(v) for v in violations.values())
    print(f"Total Violations: {total_violations}")
    print(f"Categories: {len(violations)}")
    print(f"Matched to Laws: {len(matches)}")
    print()

    print("📋 Violations by Category:")
    print("-" * 80)
    for category, items in sorted(violations.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {category}: {len(items)} violations")
    print()

    # Count by severity
    severity_counts = defaultdict(int)
    for category, items in violations.items():
        for item in items:
            severity = item.get("severity", "UNKNOWN").upper()
            severity_counts[severity] += 1

    print("⚠️  Violations by Severity:")
    print("-" * 80)
    for severity, count in sorted(severity_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {severity}: {count} violations")
    print()

    # Top entities with violations
    entity_counts = defaultdict(int)
    for category, items in violations.items():
        for item in items:
            entity = item.get("entity_name", "Unknown")
            entity_counts[entity] += 1

    print("👥 Top Entities with Violations:")
    print("-" * 80)
    top_entities = sorted(entity_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for entity, count in top_entities:
        print(f"  {entity}: {count} violations")
    print()

    # Law matches summary
    if matches:
        law_counts = defaultdict(int)
        for match in matches:
            law_name = match.get("law", {}).get("name", "Unknown")
            law_counts[law_name] += 1

        print("⚖️  Top Laws Matched:")
        print("-" * 80)
        top_laws = sorted(law_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for law, count in top_laws:
            print(f"  {law[:70]}...: {count} matches")
        print()

    # Save summary
    summary = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "total_violations": total_violations,
            "categories": len(violations),
            "matched_to_laws": len(matches)
        },
        "by_category": {cat: len(items) for cat, items in violations.items()},
        "by_severity": dict(severity_counts),
        "top_entities": dict(top_entities),
        "top_laws": dict(top_laws) if matches else {}
    }

    summary_file = DATA_PROCESSED_DIR / "violation_discovery_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"💾 Summary saved to: {summary_file}")
    print("=" * 80)


if __name__ == "__main__":
    generate_summary()
