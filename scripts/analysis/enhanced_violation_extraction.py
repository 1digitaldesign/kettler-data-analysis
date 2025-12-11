#!/usr/bin/env python3
"""
Enhanced violation extraction from cleaned lariat.txt
Extracts all violation types with context and categorization
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_RAW_DIR, DATA_PROCESSED_DIR


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    if not date_str or date_str.lower() in ['n/a', 'none', '']:
        return None

    # Try ISO format first
    try:
        return datetime.fromisoformat(date_str)
    except:
        pass

    # Try MM/DD/YYYY
    match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str.strip())
    if match:
        month, day, year = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except:
            pass

    # Try Month DD, YYYY
    month_names = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    month_match = re.match(r'(\w+)\s+(\d{1,2}),\s+(\d{4})', date_str.strip(), re.IGNORECASE)
    if month_match:
        month_name, day, year = month_match.groups()
        month_num = month_names.get(month_name.lower())
        if month_num:
            try:
                return datetime(int(year), month_num, int(day))
            except:
                pass

    return None


def calculate_days_between(date1: Optional[datetime], date2: Optional[datetime]) -> Optional[int]:
    """Calculate days between two dates"""
    if not date1 or not date2:
        return None
    return abs((date2 - date1).days)


def extract_tax_forfeitures(content: str) -> List[Dict[str, Any]]:
    """Extract tax forfeiture violations"""
    forfeitures = []
    lines = content.split('\n')

    current_filing_number = None
    current_entity_name = None

    for i, line in enumerate(lines):
        # Track current entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                current_filing_number = match.group(1)

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    current_entity_name = name_match.group(1).strip()

        # Extract tax forfeiture
        if 'Tax Forfeiture' in line:
            parts = [p.strip() for p in line.split('\t') if p.strip()]
            if len(parts) >= 3:
                document_number = parts[0] if parts[0] and parts[0] != 'N/A' else None
                filing_date_str = parts[2] if len(parts) > 2 else None
                effective_date_str = parts[3] if len(parts) > 3 else None

                filing_date = parse_date(filing_date_str) if filing_date_str else None
                effective_date = parse_date(effective_date_str) if effective_date_str else None

                forfeiture = {
                    'violation_type': 'Tax Forfeiture',
                    'severity': 'HIGH',
                    'document_number': document_number,
                    'filing_date': filing_date.isoformat() if filing_date else None,
                    'effective_date': effective_date.isoformat() if effective_date else None,
                    'entity_name': current_entity_name,
                    'filing_number': current_filing_number,
                    'description': f"Tax forfeiture for {current_entity_name} on {effective_date_str or filing_date_str}"
                }
                forfeitures.append(forfeiture)

    return forfeitures


def extract_forfeited_entities(content: str) -> List[Dict[str, Any]]:
    """Extract entities with forfeited existence status"""
    forfeited = []
    lines = content.split('\n')

    current_filing_number = None
    current_entity_name = None
    current_filing_date = None

    for i, line in enumerate(lines):
        # Track current entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                current_filing_number = match.group(1)

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    current_entity_name = name_match.group(1).strip()

        # Extract original filing date
        if 'Original Date of Filing:' in line:
            date_match = re.search(r'Original Date of Filing:\s+([^\t\n]+)', line)
            if date_match:
                current_filing_date = parse_date(date_match.group(1).strip())

        # Check for forfeited status
        if 'Entity Status:' in line and 'Forfeited existence' in line:
            status_match = re.search(r'Entity Status:\s+([^\t\n]+)', line)
            if status_match and 'Forfeited' in status_match.group(1):
                forfeited_entity = {
                    'violation_type': 'Forfeited Existence',
                    'severity': 'HIGH',
                    'entity_name': current_entity_name,
                    'filing_number': current_filing_number,
                    'status': status_match.group(1).strip(),
                    'original_filing_date': current_filing_date.isoformat() if current_filing_date else None,
                    'description': f"Entity {current_entity_name} has forfeited existence status"
                }

                # Check if already added (avoid duplicates)
                if not any(f['filing_number'] == current_filing_number for f in forfeited):
                    forfeited.append(forfeited_entity)

    return forfeited


def extract_filing_violations(content: str) -> List[Dict[str, Any]]:
    """Extract filing history violations (late filings, missing reports)"""
    violations = []
    lines = content.split('\n')

    current_filing_number = None
    current_entity_name = None
    filing_history = []

    for i, line in enumerate(lines):
        # Track current entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                # Process previous entity's filing history
                if current_filing_number and filing_history:
                    violations.extend(analyze_filing_history(
                        current_filing_number, current_entity_name, filing_history
                    ))

                current_filing_number = match.group(1)
                filing_history = []

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    current_entity_name = name_match.group(1).strip()

        # Extract filing history entries
        if 'Public Information Report (PIR)' in line or 'Certificate of Formation' in line:
            parts = [p.strip() for p in line.split('\t') if p.strip()]
            if len(parts) >= 3:
                filing_type = parts[1] if len(parts) > 1 else None
                filing_date_str = parts[2] if len(parts) > 2 else None
                effective_date_str = parts[3] if len(parts) > 3 else None

                filing_date = parse_date(filing_date_str) if filing_date_str else None
                effective_date = parse_date(effective_date_str) if effective_date_str else None

                filing_history.append({
                    'type': filing_type,
                    'filing_date': filing_date,
                    'effective_date': effective_date,
                    'filing_date_str': filing_date_str,
                    'effective_date_str': effective_date_str
                })

    # Process last entity
    if current_filing_number and filing_history:
        violations.extend(analyze_filing_history(
            current_filing_number, current_entity_name, filing_history
        ))

    return violations


def analyze_filing_history(filing_number: str, entity_name: str, history: List[Dict]) -> List[Dict[str, Any]]:
    """Analyze filing history for violations"""
    violations = []

    # Group PIR filings by year
    pir_filings = [f for f in history if f.get('type') == 'Public Information Report (PIR)']

    # Check for late filings (filing date after effective date)
    for filing in pir_filings:
        filing_date = filing.get('filing_date')
        effective_date = filing.get('effective_date')

        if filing_date and effective_date:
            # If filing date is significantly after effective date, it's late
            days_late = (filing_date - effective_date).days
            if days_late > 30:  # More than 30 days late
                violations.append({
                    'violation_type': 'Late Filing',
                    'severity': 'MEDIUM',
                    'entity_name': entity_name,
                    'filing_number': filing_number,
                    'filing_type': filing.get('type'),
                    'filing_date': filing_date.isoformat(),
                    'effective_date': effective_date.isoformat(),
                    'days_late': days_late,
                    'description': f"Late filing: {days_late} days after effective date"
                })

    # Check for missing annual PIRs (should be filed annually)
    if len(pir_filings) > 1:
        pir_filings_sorted = sorted(
            [f for f in pir_filings if f.get('filing_date')],
            key=lambda x: x['filing_date']
        )

        for i in range(len(pir_filings_sorted) - 1):
            current = pir_filings_sorted[i]['filing_date']
            next_filing = pir_filings_sorted[i + 1]['filing_date']

            # Check if gap is more than 400 days (allowing some flexibility)
            gap_days = (next_filing - current).days
            if gap_days > 400:
                violations.append({
                    'violation_type': 'Missing Annual Filing',
                    'severity': 'MEDIUM',
                    'entity_name': entity_name,
                    'filing_number': filing_number,
                    'gap_days': gap_days,
                    'last_filing': current.isoformat(),
                    'next_filing': next_filing.isoformat(),
                    'description': f"Gap of {gap_days} days between PIR filings (expected ~365 days)"
                })

    return violations


def extract_address_violations(content: str) -> List[Dict[str, Any]]:
    """Extract address clustering violations"""
    violations = []
    address_to_entities = defaultdict(list)
    lines = content.split('\n')

    current_filing_number = None
    current_entity_name = None
    current_address = None

    for i, line in enumerate(lines):
        # Track current entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                current_filing_number = match.group(1)

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    current_entity_name = name_match.group(1).strip()

        # Extract address
        if 'Address:' in line:
            addr_match = re.search(r'Address:\s+([^\t\n]+)', line)
            if addr_match:
                current_address = addr_match.group(1).strip().upper()
                if current_address and current_filing_number:
                    address_to_entities[current_address].append({
                        'filing_number': current_filing_number,
                        'entity_name': current_entity_name
                    })

    # Identify address clusters (multiple entities at same address)
    for address, entities in address_to_entities.items():
        if len(entities) > 1:
            violations.append({
                'violation_type': 'Address Clustering',
                'severity': 'MEDIUM',
                'address': address,
                'entity_count': len(entities),
                'entities': entities,
                'description': f"{len(entities)} entities share the same address: {address}"
            })

    return violations


def extract_management_violations(content: str) -> List[Dict[str, Any]]:
    """Extract management-related violations"""
    violations = []
    lines = content.split('\n')

    current_filing_number = None
    current_entity_name = None
    management_changes = []
    forfeiture_dates = []

    for i, line in enumerate(lines):
        # Track current entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                # Process previous entity
                if current_filing_number and management_changes and forfeiture_dates:
                    violations.extend(analyze_management_violations(
                        current_filing_number, current_entity_name,
                        management_changes, forfeiture_dates
                    ))

                current_filing_number = match.group(1)
                management_changes = []
                forfeiture_dates = []

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    current_entity_name = name_match.group(1).strip()

        # Track tax forfeitures
        if 'Tax Forfeiture' in line:
            parts = [p.strip() for p in line.split('\t') if p.strip()]
            if len(parts) >= 3:
                date_str = parts[3] if len(parts) > 3 else parts[2]
                forfeiture_date = parse_date(date_str)
                if forfeiture_date:
                    forfeiture_dates.append(forfeiture_date)

        # Track management entries
        if 'Last Update' in line and 'Name' in line and 'Title' in line:
            # Next few lines contain management data
            for j in range(i+1, min(i+10, len(lines))):
                mgmt_line = lines[j]
                if mgmt_line.strip() and '\t' in mgmt_line:
                    parts = [p.strip() for p in mgmt_line.split('\t') if p.strip()]
                    if len(parts) >= 3:
                        update_date = parse_date(parts[0])
                        mgmt_name = parts[1] if len(parts) > 1 else None
                        title = parts[2] if len(parts) > 2 else None

                        if update_date:
                            management_changes.append({
                                'date': update_date,
                                'name': mgmt_name,
                                'title': title
                            })
                    break

    # Process last entity
    if current_filing_number and management_changes and forfeiture_dates:
        violations.extend(analyze_management_violations(
            current_filing_number, current_entity_name,
            management_changes, forfeiture_dates
        ))

    return violations


def analyze_management_violations(filing_number: str, entity_name: str,
                                 management_changes: List[Dict],
                                 forfeiture_dates: List[datetime]) -> List[Dict[str, Any]]:
    """Analyze management changes for violations"""
    violations = []

    # Check if management changed during forfeiture period
    for forfeiture_date in forfeiture_dates:
        # Look for management changes within 90 days of forfeiture
        for mgmt_change in management_changes:
            days_diff = abs((mgmt_change['date'] - forfeiture_date).days)
            if days_diff <= 90:
                violations.append({
                    'violation_type': 'Management Change During Forfeiture',
                    'severity': 'HIGH',
                    'entity_name': entity_name,
                    'filing_number': filing_number,
                    'forfeiture_date': forfeiture_date.isoformat(),
                    'management_change_date': mgmt_change['date'].isoformat(),
                    'days_difference': days_diff,
                    'management_name': mgmt_change.get('name'),
                    'description': f"Management change occurred {days_diff} days around forfeiture date"
                })

    return violations


def main():
    """Main violation extraction function"""
    print("=" * 60)
    print("Enhanced Violation Extraction")
    print("=" * 60)

    # Load cleaned data
    cleaned_file = DATA_PROCESSED_DIR / "lariat_entities_cleaned.json"
    if not cleaned_file.exists():
        print(f"Error: {cleaned_file} not found. Run preprocess_violation_data.py first.")
        return

    # Read raw text for detailed extraction
    lariat_txt = DATA_RAW_DIR / "lariat.txt"
    if not lariat_txt.exists():
        print(f"Error: {lariat_txt} not found")
        return

    with open(lariat_txt, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nExtracting violations...")

    # Extract all violation types
    tax_forfeitures = extract_tax_forfeitures(content)
    print(f"  Found {len(tax_forfeitures)} tax forfeitures")

    forfeited_entities = extract_forfeited_entities(content)
    print(f"  Found {len(forfeited_entities)} forfeited entities")

    filing_violations = extract_filing_violations(content)
    print(f"  Found {len(filing_violations)} filing violations")

    address_violations = extract_address_violations(content)
    print(f"  Found {len(address_violations)} address clustering violations")

    management_violations = extract_management_violations(content)
    print(f"  Found {len(management_violations)} management violations")

    # Combine all violations
    all_violations = {
        'tax_forfeitures': tax_forfeitures,
        'forfeited_entities': forfeited_entities,
        'filing_violations': filing_violations,
        'address_violations': address_violations,
        'management_violations': management_violations
    }

    # Categorize by entity
    violations_by_entity = defaultdict(list)
    for violation_type, violations in all_violations.items():
        for violation in violations:
            filing_num = violation.get('filing_number')
            if filing_num:
                violations_by_entity[filing_num].append({
                    'type': violation_type,
                    'violation': violation
                })

    # Generate summary
    total_violations = sum(len(v) for v in all_violations.values())
    high_severity = sum(1 for v_list in all_violations.values()
                       for v in v_list if v.get('severity') == 'HIGH')
    medium_severity = sum(1 for v_list in all_violations.values()
                          for v in v_list if v.get('severity') == 'MEDIUM')

    summary = {
        'total_violations': total_violations,
        'high_severity': high_severity,
        'medium_severity': medium_severity,
        'entities_with_violations': len(violations_by_entity),
        'violations_by_type': {k: len(v) for k, v in all_violations.items()}
    }

    # Save results
    output_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    with open(output_file, 'w') as f:
        json.dump({
            'violations': all_violations,
            'violations_by_entity': dict(violations_by_entity),
            'summary': summary,
            'metadata': {
                'generated': datetime.now().isoformat(),
                'source': 'enhanced_violation_extraction.py'
            }
        }, f, indent=2, default=str)

    print(f"\n✓ Violation extraction complete!")
    print(f"  Total violations: {total_violations}")
    print(f"  High severity: {high_severity}")
    print(f"  Medium severity: {medium_severity}")
    print(f"  Entities with violations: {len(violations_by_entity)}")
    print(f"  Saved to: {output_file}")


if __name__ == '__main__':
    main()
