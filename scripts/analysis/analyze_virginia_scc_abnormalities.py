#!/usr/bin/env python3
"""
Analyze Virginia SCC filings for abnormalities using pattern matching and semantic analysis
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent

def load_virginia_scc_data() -> Dict[str, Any]:
    """Load Virginia SCC raw data"""
    raw_file = PROJECT_ROOT / "data" / "raw" / "virginia_scc_kettler_filings.json"
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw data file not found: {raw_file}")

    with open(raw_file, 'r') as f:
        return json.load(f)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using word overlap"""
    words1 = set(text1.upper().split())
    words2 = set(text2.upper().split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union) if union else 0.0

def analyze_name_abnormalities(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze entity names for abnormalities"""
    abnormalities = []

    legal_name = entity.get("legal_name", "").strip()
    fictitious_name = entity.get("fictitious_name", "").strip()

    if legal_name and fictitious_name:
        # Calculate similarity
        similarity = calculate_text_similarity(legal_name, fictitious_name)

        # Extract corporate suffixes
        legal_suffix = ""
        fict_suffix = ""

        if "INC" in legal_name.upper() or "INCORPORATED" in legal_name.upper():
            legal_suffix = "INC"
        elif "LLC" in legal_name.upper():
            legal_suffix = "LLC"
        elif "CORP" in legal_name.upper() or "CORPORATION" in legal_name.upper():
            legal_suffix = "CORP"

        if "INC" in fictitious_name.upper() or "INCORPORATED" in fictitious_name.upper():
            fict_suffix = "INC"
        elif "LLC" in fictitious_name.upper():
            fict_suffix = "LLC"
        elif "CORP" in fictitious_name.upper() or "CORPORATION" in fictitious_name.upper():
            fict_suffix = "CORP"

        # Check for suffix mismatch
        if legal_suffix and fict_suffix and legal_suffix != fict_suffix:
            abnormalities.append({
                "category": "Corporate Suffix Mismatch",
                "severity": "Medium",
                "description": f"Legal name uses '{legal_suffix}' but fictitious name uses '{fict_suffix}'. High similarity ({similarity:.2%}) suggests intentional variation.",
                "legal_name": legal_name,
                "fictitious_name": fictitious_name,
                "similarity_score": similarity,
                "legal_suffix": legal_suffix,
                "fictitious_suffix": fict_suffix,
                "implication": "May be used to create confusion or separate business identities. Verify proper DBA registration and disclosure."
            })

        # Check for high similarity with different suffixes
        if similarity > 0.85 and legal_suffix != fict_suffix:
            abnormalities.append({
                "category": "High Name Similarity with Different Suffixes",
                "severity": "Medium",
                "description": f"Names are {similarity:.1%} similar but use different corporate suffixes. This pattern is unusual.",
                "similarity_score": similarity,
                "implication": "Could indicate attempt to operate under multiple identities or create regulatory separation"
            })

    return abnormalities

def analyze_address_abnormalities(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze address for abnormalities"""
    abnormalities = []

    address = entity.get("business_address", "").strip()
    if not address:
        return abnormalities

    address_lower = address.lower()

    # Check for suite/ste patterns
    if "ste" in address_lower or "suite" in address_lower:
        abnormalities.append({
            "category": "Suite Address Pattern",
            "severity": "Low",
            "description": "Business address uses suite designation",
            "address": address,
            "pattern": "Suite/Ste",
            "implication": "Common for office buildings, but verify if this is actual business location vs. mail forwarding service"
        })

    # Check for registered agent address patterns
    registered_agent = entity.get("registered_agent", "").lower()
    if "registered agents" in registered_agent or "ra " in registered_agent:
        # Check if address matches registered agent location
        if "virginia" not in address_lower or "va" not in address_lower:
            abnormalities.append({
                "category": "Registered Agent Address Mismatch",
                "severity": "Low",
                "description": "Uses commercial registered agent but address may not match agent location",
                "address": address,
                "registered_agent": entity.get("registered_agent"),
                "implication": "Standard practice, but verify actual business location"
            })

    # Check for PO Box (not found in this case, but check anyway)
    if "p.o." in address_lower or "po box" in address_lower or "pobox" in address_lower:
        abnormalities.append({
            "category": "PO Box Address",
            "severity": "Medium",
            "description": "Business address is a PO Box",
            "address": address,
            "implication": "PO Box addresses may indicate mail forwarding or lack of physical presence"
        })

    return abnormalities

def analyze_registered_agent_abnormalities(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze registered agent for abnormalities"""
    abnormalities = []

    registered_agent = entity.get("registered_agent", "").strip()
    if not registered_agent:
        return abnormalities

    agent_lower = registered_agent.lower()

    # Check for commercial registered agent services
    commercial_agent_patterns = [
        "registered agents",
        "ra ",
        "corp",
        "incorporation services",
        "business services"
    ]

    is_commercial = any(pattern in agent_lower for pattern in commercial_agent_patterns)

    if is_commercial:
        abnormalities.append({
            "category": "Commercial Registered Agent",
            "severity": "Low",
            "description": "Uses commercial registered agent service",
            "registered_agent": registered_agent,
            "implication": "Standard practice for privacy/legal purposes, but may obscure actual business location and control"
        })

    # Check if registered agent name is similar to entity name (potential self-registration)
    entity_name = entity.get("legal_name", "").lower()
    if entity_name and registered_agent.lower() in entity_name:
        abnormalities.append({
            "category": "Self-Registered Agent",
            "severity": "Low",
            "description": "Registered agent name appears in entity name",
            "registered_agent": registered_agent,
            "entity_name": entity.get("legal_name"),
            "implication": "May indicate self-registration, verify actual agent relationship"
        })

    return abnormalities

def analyze_missing_information(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze missing information"""
    abnormalities = []

    missing_fields = []
    critical_fields = {
        "formation_date": "Formation Date",
        "last_annual_report": "Last Annual Report Date"
    }

    for field, display_name in critical_fields.items():
        if not entity.get(field):
            missing_fields.append(display_name)

    if missing_fields:
        abnormalities.append({
            "category": "Missing Critical Information",
            "severity": "Medium",
            "description": f"Missing fields: {', '.join(missing_fields)}",
            "missing_fields": missing_fields,
            "implication": "Cannot verify entity history, compliance timeline, or annual report filing status without this information"
        })

    return abnormalities

def analyze_entity_type_abnormalities(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze entity type for abnormalities"""
    abnormalities = []

    entity_type = entity.get("entity_type", "").strip()
    status = entity.get("status", "").strip()

    # Check entity type consistency
    if entity_type == "Stock Corporation":
        abnormalities.append({
            "category": "Stock Corporation Structure",
            "severity": "Low",
            "description": "Entity is a Stock Corporation",
            "entity_type": entity_type,
            "implication": "Stock corporations typically have shareholders and board of directors. Verify shareholder structure and control."
        })

    # Check status
    if status.lower() != "active":
        abnormalities.append({
            "category": "Non-Active Status",
            "severity": "High",
            "description": f"Entity status is '{status}', not 'Active'",
            "status": status,
            "implication": "Non-active status may indicate compliance issues, dissolution, or administrative action"
        })

    return abnormalities

def analyze_pattern_abnormalities(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze for suspicious patterns"""
    abnormalities = []

    # Combine all text fields for pattern analysis
    all_text = " ".join([
        entity.get("legal_name", ""),
        entity.get("fictitious_name", ""),
        entity.get("entity_type", ""),
        entity.get("business_address", ""),
        entity.get("registered_agent", ""),
        entity.get("notes", "")
    ]).lower()

    # Check for suspicious keywords
    suspicious_patterns = {
        "shell": "Shell company indicators",
        "holding": "Holding company structure",
        "dormant": "Dormant entity",
        "inactive": "Inactive status",
        "dissolved": "Dissolved entity"
    }

    found_patterns = []
    for pattern, description in suspicious_patterns.items():
        if pattern in all_text:
            found_patterns.append({
                "pattern": pattern,
                "description": description
            })

    if found_patterns:
        abnormalities.append({
            "category": "Suspicious Patterns",
            "severity": "High",
            "description": f"Found suspicious patterns: {', '.join([p['pattern'] for p in found_patterns])}",
            "patterns": found_patterns,
            "implication": "May indicate shell company, holding structure, or inactive entity"
        })

    # Check for common shell company indicators
    shell_indicators = []

    # Same address as registered agent (common shell company pattern)
    address = entity.get("business_address", "").lower()
    registered_agent = entity.get("registered_agent", "").lower()

    # Check if address contains registered agent company name
    if registered_agent and any(word in address for word in registered_agent.split() if len(word) > 3):
        shell_indicators.append("Address may be same as registered agent location")

    if shell_indicators:
        abnormalities.append({
            "category": "Potential Shell Company Indicators",
            "severity": "Medium",
            "description": "Found indicators that may suggest shell company structure",
            "indicators": shell_indicators,
            "implication": "Further investigation needed to verify actual business operations"
        })

    return abnormalities

def main():
    """Main function"""
    print("=" * 70)
    print("Virginia SCC Filings - Advanced Abnormality Analysis")
    print("=" * 70)

    # Load data
    print("\n1. Loading Virginia SCC data...")
    data = load_virginia_scc_data()
    entities = data.get("entities_found", [])
    print(f"   ✓ Loaded data for {len(entities)} entities")

    if not entities:
        print("   ✗ No entities found in data")
        return

    entity = entities[0]

    # Run all analyses
    print("\n2. Running abnormality analyses...")
    all_abnormalities = []

    all_abnormalities.extend(analyze_name_abnormalities(entity))
    all_abnormalities.extend(analyze_address_abnormalities(entity))
    all_abnormalities.extend(analyze_registered_agent_abnormalities(entity))
    all_abnormalities.extend(analyze_missing_information(entity))
    all_abnormalities.extend(analyze_entity_type_abnormalities(entity))
    all_abnormalities.extend(analyze_pattern_abnormalities(entity))

    # Categorize by severity
    high_severity = [a for a in all_abnormalities if a.get("severity") == "High"]
    medium_severity = [a for a in all_abnormalities if a.get("severity") == "Medium"]
    low_severity = [a for a in all_abnormalities if a.get("severity") == "Low"]

    print(f"   ✓ Found {len(all_abnormalities)} abnormalities")
    print(f"     - High severity: {len(high_severity)}")
    print(f"     - Medium severity: {len(medium_severity)}")
    print(f"     - Low severity: {len(low_severity)}")

    # Create analysis results
    analysis_results = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "source": "Virginia SCC Advanced Pattern Analysis",
            "entity_id": entity.get("entity_id"),
            "analysis_method": "Pattern matching and semantic analysis"
        },
        "entity_data": entity,
        "abnormalities": all_abnormalities,
        "summary": {
            "total_abnormalities": len(all_abnormalities),
            "high_severity": len(high_severity),
            "medium_severity": len(medium_severity),
            "low_severity": len(low_severity),
            "abnormalities_by_category": {}
        }
    }

    # Group by category
    for abnormality in all_abnormalities:
        category = abnormality.get("category", "Unknown")
        if category not in analysis_results["summary"]["abnormalities_by_category"]:
            analysis_results["summary"]["abnormalities_by_category"][category] = 0
        analysis_results["summary"]["abnormalities_by_category"][category] += 1

    # Save results
    output_file = PROJECT_ROOT / "research" / "analysis" / "virginia_scc_advanced_abnormalities.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)

    print(f"\n3. Saving results to {output_file}")
    print(f"   ✓ Results saved")

    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)

    for i, abnormality in enumerate(all_abnormalities, 1):
        severity_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(abnormality.get("severity"), "⚪")
        print(f"\n{i}. {severity_icon} {abnormality['category']} ({abnormality['severity']} Severity)")
        print(f"   {abnormality['description']}")
        if 'implication' in abnormality:
            print(f"   Implication: {abnormality['implication']}")

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)

    return analysis_results

if __name__ == "__main__":
    main()
