#!/usr/bin/env python3
"""
Preprocess violation data: clean, enrich, and validate
Combines raw Texas filing data with research directory intersections
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import hashlib

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import (
    PROJECT_ROOT, DATA_DIR, DATA_RAW_DIR, DATA_VECTORS_DIR,
    RESEARCH_DIR, DATA_CLEANED_DIR
)

# Create processed directory
DATA_PROCESSED_DIR = DATA_DIR / "processed"
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def normalize_entity_name(name: str) -> str:
    """Normalize entity name"""
    if not name:
        return ""
    # Remove extra whitespace, standardize capitalization
    name = re.sub(r'\s+', ' ', name.strip())
    # Title case for consistency
    return name.title()


def normalize_date(date_str: str) -> Optional[str]:
    """Convert date to ISO format (YYYY-MM-DD)"""
    if not date_str or date_str.lower() in ['n/a', 'none', '']:
        return None

    # Common date formats
    patterns = [
        (r'(\d{1,2})/(\d{1,2})/(\d{4})', r'\3-\1-\2'),  # MM/DD/YYYY
        (r'(\w+)\s+(\d{1,2}),\s+(\d{4})', None),  # Month DD, YYYY - needs month name mapping
        (r'(\d{4})-(\d{2})-(\d{2})', r'\1-\2-\3'),  # Already ISO
    ]

    # Try ISO format first
    iso_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_str.strip())
    if iso_match:
        return date_str.strip()

    # Try MM/DD/YYYY
    slash_match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str.strip())
    if slash_match:
        month, day, year = slash_match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Month name format (e.g., "February 8, 2013")
    month_names = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    month_match = re.match(r'(\w+)\s+(\d{1,2}),\s+(\d{4})', date_str.strip(), re.IGNORECASE)
    if month_match:
        month_name, day, year = month_match.groups()
        month_num = month_names.get(month_name.lower())
        if month_num:
            return f"{year}-{month_num}-{day.zfill(2)}"

    # Return as-is if can't parse (will be flagged in validation)
    return date_str.strip()


def normalize_address(address: str) -> str:
    """Normalize address format"""
    if not address:
        return ""

    # Normalize street abbreviations
    abbrevs = {
        'ST': 'STREET', 'ST.': 'STREET',
        'AVE': 'AVENUE', 'AVE.': 'AVENUE',
        'RD': 'ROAD', 'RD.': 'ROAD',
        'DR': 'DRIVE', 'DR.': 'DRIVE',
        'BLVD': 'BOULEVARD', 'BLVD.': 'BOULEVARD',
        'LN': 'LANE', 'LN.': 'LANE',
        'CT': 'COURT', 'CT.': 'COURT',
        'PL': 'PLACE', 'PL.': 'PLACE',
        'STE': 'SUITE', 'STE.': 'SUITE',
        'APT': 'APARTMENT', 'APT.': 'APARTMENT',
    }

    # Normalize whitespace
    address = re.sub(r'\s+', ' ', address.strip().upper())

    # Replace abbreviations
    for abbrev, full in abbrevs.items():
        address = re.sub(rf'\b{abbrev}\b', full, address, flags=re.IGNORECASE)

    # Normalize zip codes (5 digits or 5-4 format)
    address = re.sub(r'(\d{5})(?:-(\d{4}))?', r'\1\2', address)

    return address


def validate_tax_id(tax_id: str) -> bool:
    """Validate Texas Tax ID format (11 digits)"""
    if not tax_id:
        return False
    return bool(re.match(r'^\d{11}$', str(tax_id).strip()))


def validate_fein(fein: str) -> bool:
    """Validate FEIN format (9 digits, may have dashes)"""
    if not fein:
        return False
    cleaned = re.sub(r'[-\s]', '', str(fein).strip())
    return bool(re.match(r'^\d{9}$', cleaned))


def clean_raw_text_data(file_path: Path) -> Dict[str, Any]:
    """Clean raw lariat.txt data"""
    print(f"Cleaning raw text data from: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entities = {}
    current_filing_number = None
    current_entity = None

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detect new entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                filing_num = match.group(1)
                current_filing_number = filing_num

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match:
                    # Check next lines
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    entity_name = normalize_entity_name(name_match.group(1))
                    if filing_num not in entities:
                        entities[filing_num] = {
                            'filing_number': filing_num,
                            'name': entity_name,
                            'status': None,
                            'entity_type': None,
                            'tax_id': None,
                            'fein': None,
                            'address': None,
                            'original_filing_date': None,
                            'filing_history': [],
                            'management': [],
                            'registered_agent': None
                        }
                    current_entity = entities[filing_num]

        elif current_entity:
            # Extract entity status
            if 'Entity Status:' in line:
                status_match = re.search(r'Entity Status:\s+([^\t\n]+)', line)
                if status_match:
                    current_entity['status'] = status_match.group(1).strip()

            # Extract entity type
            if 'Entity Type:' in line:
                type_match = re.search(r'Entity Type:\s+([^\t\n]+)', line)
                if type_match:
                    current_entity['entity_type'] = type_match.group(1).strip()

            # Extract Tax ID
            if 'Tax ID:' in line:
                tax_match = re.search(r'Tax ID:\s+(\d+)', line)
                if tax_match:
                    tax_id = tax_match.group(1).strip()
                    if validate_tax_id(tax_id):
                        current_entity['tax_id'] = tax_id

            # Extract FEIN
            if 'FEIN:' in line:
                fein_match = re.search(r'FEIN:\s+([\d-]+)', line)
                if fein_match:
                    fein = fein_match.group(1).strip()
                    if validate_fein(fein):
                        current_entity['fein'] = fein

            # Extract address
            if 'Address:' in line:
                addr_match = re.search(r'Address:\s+([^\t\n]+)', line)
                if addr_match:
                    address = normalize_address(addr_match.group(1))
                    if address:
                        current_entity['address'] = address

            # Extract original filing date
            if 'Original Date of Filing:' in line:
                date_match = re.search(r'Original Date of Filing:\s+([^\t\n]+)', line)
                if date_match:
                    date_str = normalize_date(date_match.group(1).strip())
                    current_entity['original_filing_date'] = date_str

            # Extract filing history (Tax Forfeiture, etc.)
            if 'Tax Forfeiture' in line:
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 3:
                    forfeiture = {
                        'document_number': parts[0] if parts[0] else None,
                        'filing_type': 'Tax Forfeiture',
                        'filing_date': normalize_date(parts[2]) if len(parts) > 2 else None,
                        'effective_date': normalize_date(parts[3]) if len(parts) > 3 else None
                    }
                    current_entity['filing_history'].append(forfeiture)

    print(f"  Cleaned {len(entities)} entities")
    return {'entities': entities}


def clean_embeddings_data(file_path: Path) -> Dict[str, Any]:
    """Clean and validate embeddings data"""
    print(f"Cleaning embeddings data from: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = data.get('metadata', {})
    vectors = data.get('vectors', [])

    # Validate metadata
    expected_dim = metadata.get('dimension', 384)
    cleaned_vectors = []
    entity_ids = set()

    for vec in vectors:
        entity_id = vec.get('id', '')
        embedding = vec.get('embedding', [])

        # Validate embedding dimension
        if len(embedding) != expected_dim:
            print(f"  Warning: Entity {entity_id} has incorrect dimension: {len(embedding)}")
            continue

        # Check for duplicates
        if entity_id in entity_ids:
            print(f"  Warning: Duplicate entity ID: {entity_id}")
            continue

        entity_ids.add(entity_id)

        # Normalize entity ID
        normalized_id = entity_id.replace('lariat_tx_', '')

        cleaned_vectors.append({
            'id': normalized_id,
            'original_id': entity_id,
            'text': vec.get('text', ''),
            'embedding': embedding,
            'metadata': vec.get('metadata', {})
        })

    print(f"  Cleaned {len(cleaned_vectors)} embeddings")

    return {
        'metadata': metadata,
        'vectors': cleaned_vectors
    }


def load_research_data() -> Dict[str, Any]:
    """Load and structure research directory data"""
    print("Loading research directory data...")

    research_data = {
        'connections': [],
        'license_searches': {},
        'employees': {},
        'company_registrations': [],
        'financial': [],
        'fraud_indicators': {},
        'all_entities': {},
        'all_individuals': {}
    }

    # Load connections
    connections_dir = RESEARCH_DIR / "connections"
    if connections_dir.exists():
        for conn_file in connections_dir.glob("*.json"):
            try:
                with open(conn_file, 'r') as f:
                    data = json.load(f)
                    research_data['connections'].append(data)
            except Exception as e:
                print(f"  Warning: Could not load {conn_file}: {e}")

    # Load fraud indicators
    fraud_file = RESEARCH_DIR / "fraud_indicators.json"
    if fraud_file.exists():
        try:
            with open(fraud_file, 'r') as f:
                research_data['fraud_indicators'] = json.load(f)
        except Exception as e:
            print(f"  Warning: Could not load fraud indicators: {e}")

    # Load all entities
    entities_file = RESEARCH_DIR / "all_entities_extracted.json"
    if entities_file.exists():
        try:
            with open(entities_file, 'r') as f:
                data = json.load(f)
                # Convert to dict keyed by entity name if it's a list
                if isinstance(data, list):
                    for entity in data:
                        if 'name' in entity:
                            research_data['all_entities'][entity['name']] = entity
                elif isinstance(data, dict):
                    research_data['all_entities'] = data
        except Exception as e:
            print(f"  Warning: Could not load all entities: {e}")

    # Load all individuals
    individuals_file = RESEARCH_DIR / "all_individuals_identified.json"
    if individuals_file.exists():
        try:
            with open(individuals_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for individual in data:
                        if 'name' in individual:
                            research_data['all_individuals'][individual['name']] = individual
                elif isinstance(data, dict):
                    research_data['all_individuals'] = data
        except Exception as e:
            print(f"  Warning: Could not load all individuals: {e}")

    # Load license searches (sample from each state)
    license_dir = RESEARCH_DIR / "license_searches"
    if license_dir.exists():
        for state_dir in license_dir.iterdir():
            if state_dir.is_dir():
                state_name = state_dir.name
                research_data['license_searches'][state_name] = []
                for license_file in list(state_dir.glob("*.json"))[:5]:  # Sample first 5
                    try:
                        with open(license_file, 'r') as f:
                            research_data['license_searches'][state_name].append(json.load(f))
                    except Exception as e:
                        print(f"  Warning: Could not load {license_file}: {e}")

    print(f"  Loaded research data: {len(research_data['connections'])} connections, "
          f"{len(research_data['fraud_indicators'])} fraud indicators, "
          f"{len(research_data['all_entities'])} entities, "
          f"{len(research_data['all_individuals'])} individuals")

    return research_data


def enrich_entities_with_research(entities: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich entity data with research intersections"""
    print("Enriching entities with research data...")

    enriched_entities = {}

    for filing_num, entity in entities.items():
        enriched = entity.copy()
        enriched['research_intersections'] = {
            'connections': [],
            'license_searches': [],
            'employees': [],
            'company_registrations': [],
            'financial': [],
            'fraud_indicators': [],
            'matched_entities': [],
            'matched_individuals': []
        }

        entity_name = entity.get('name', '').upper()

        # Match with all_entities
        if entity_name in research_data['all_entities']:
            enriched['research_intersections']['matched_entities'].append(
                research_data['all_entities'][entity_name]
            )

        # Match with connections (by name or address)
        entity_address = entity.get('address', '').upper()
        for conn in research_data['connections']:
            # Simple name matching
            if entity_name and entity_name in str(conn).upper():
                enriched['research_intersections']['connections'].append(conn)

        # Match with fraud indicators
        fraud_data = research_data.get('fraud_indicators', {})
        if 'address_clusters' in fraud_data:
            for cluster in fraud_data['address_clusters']:
                cluster_addr = cluster.get('Address', '').upper()
                if entity_address and cluster_addr in entity_address:
                    enriched['research_intersections']['fraud_indicators'].append({
                        'type': 'address_cluster',
                        'data': cluster
                    })

        # Match management names with all_individuals
        for mgmt in entity.get('management', []):
            mgmt_name = mgmt.get('name', '').upper()
            if mgmt_name in research_data['all_individuals']:
                enriched['research_intersections']['matched_individuals'].append({
                    'management_name': mgmt_name,
                    'individual_data': research_data['all_individuals'][mgmt_name]
                })

        enriched_entities[filing_num] = enriched

    print(f"  Enriched {len(enriched_entities)} entities")
    return enriched_entities


def calculate_data_quality(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate data quality metrics"""
    print("Calculating data quality metrics...")

    total_entities = len(entities)
    if total_entities == 0:
        return {'error': 'No entities to analyze'}

    quality_metrics = {
        'total_entities': total_entities,
        'completeness': {},
        'consistency': {},
        'accuracy': {},
        'uniqueness': {}
    }

    # Completeness: percentage of fields populated
    required_fields = ['name', 'status', 'entity_type', 'tax_id', 'address', 'original_filing_date']
    for field in required_fields:
        populated = sum(1 for e in entities.values() if e.get(field))
        quality_metrics['completeness'][field] = {
            'populated': populated,
            'percentage': (populated / total_entities * 100) if total_entities > 0 else 0
        }

    # Consistency: check for duplicate names with different filing numbers
    name_to_filings = defaultdict(list)
    for filing_num, entity in entities.items():
        name = entity.get('name', '').upper()
        if name:
            name_to_filings[name].append(filing_num)

    duplicates = {name: filings for name, filings in name_to_filings.items() if len(filings) > 1}
    quality_metrics['consistency']['duplicate_names'] = {
        'count': len(duplicates),
        'details': duplicates
    }

    # Accuracy: validate dates, tax IDs
    valid_dates = 0
    valid_tax_ids = 0
    for entity in entities.values():
        if entity.get('original_filing_date'):
            try:
                datetime.fromisoformat(entity['original_filing_date'])
                valid_dates += 1
            except:
                pass

        if entity.get('tax_id') and validate_tax_id(entity['tax_id']):
            valid_tax_ids += 1

    quality_metrics['accuracy'] = {
        'valid_dates': valid_dates,
        'valid_tax_ids': valid_tax_ids,
        'date_accuracy': (valid_dates / total_entities * 100) if total_entities > 0 else 0,
        'tax_id_accuracy': (valid_tax_ids / total_entities * 100) if total_entities > 0 else 0
    }

    # Uniqueness: check for duplicate filing numbers (shouldn't happen)
    filing_numbers = [e.get('filing_number') for e in entities.values()]
    unique_filings = len(set(filing_numbers))
    quality_metrics['uniqueness'] = {
        'unique_filing_numbers': unique_filings,
        'duplicate_count': len(filing_numbers) - unique_filings
    }

    # Overall quality score
    completeness_avg = sum(m['percentage'] for m in quality_metrics['completeness'].values()) / len(quality_metrics['completeness'])
    quality_metrics['overall_score'] = {
        'completeness': completeness_avg,
        'consistency_score': 100 - (len(duplicates) / total_entities * 100) if total_entities > 0 else 100,
        'accuracy_score': (quality_metrics['accuracy']['date_accuracy'] + quality_metrics['accuracy']['tax_id_accuracy']) / 2,
        'uniqueness_score': (unique_filings / total_entities * 100) if total_entities > 0 else 100
    }

    print(f"  Overall quality score: {quality_metrics['overall_score']}")
    return quality_metrics


def create_entity_relationship_graph(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Create entity relationship graph"""
    print("Creating entity relationship graph...")

    graph = {
        'nodes': [],
        'edges': []
    }

    # Add nodes
    for filing_num, entity in entities.items():
        graph['nodes'].append({
            'id': filing_num,
            'name': entity.get('name'),
            'status': entity.get('status'),
            'entity_type': entity.get('entity_type')
        })

    # Add edges based on shared addresses, agents, management
    address_to_entities = defaultdict(list)
    agent_to_entities = defaultdict(list)

    for filing_num, entity in entities.items():
        address = entity.get('address', '').upper()

        # Handle registered_agent which might be dict, string, or None
        agent = None
        registered_agent = entity.get('registered_agent')
        if isinstance(registered_agent, dict):
            agent = registered_agent.get('name', '').upper()
        elif isinstance(registered_agent, str):
            agent = registered_agent.upper()

        if address:
            address_to_entities[address].append(filing_num)
        if agent:
            agent_to_entities[agent].append(filing_num)

    edge_id = 0
    # Address-based edges
    for address, entity_list in address_to_entities.items():
        if len(entity_list) > 1:
            for i, e1 in enumerate(entity_list):
                for e2 in entity_list[i+1:]:
                    graph['edges'].append({
                        'id': f'edge_{edge_id}',
                        'source': e1,
                        'target': e2,
                        'type': 'shared_address',
                        'weight': 1.0
                    })
                    edge_id += 1

    # Agent-based edges
    for agent, entity_list in agent_to_entities.items():
        if len(entity_list) > 1:
            for i, e1 in enumerate(entity_list):
                for e2 in entity_list[i+1:]:
                    graph['edges'].append({
                        'id': f'edge_{edge_id}',
                        'source': e1,
                        'target': e2,
                        'type': 'shared_agent',
                        'weight': 1.0
                    })
                    edge_id += 1

    print(f"  Created graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
    return graph


def main():
    """Main preprocessing function"""
    print("=" * 60)
    print("Violation Data Preprocessing Pipeline")
    print("=" * 60)

    # Paths
    lariat_txt = DATA_RAW_DIR / "lariat.txt"
    embeddings_file = DATA_VECTORS_DIR / "lariat_tx_embeddings.json"

    if not lariat_txt.exists():
        print(f"Error: {lariat_txt} not found")
        return

    if not embeddings_file.exists():
        print(f"Warning: {embeddings_file} not found, skipping embeddings cleaning")
        embeddings_data = None
    else:
        embeddings_data = clean_embeddings_data(embeddings_file)

    # Step 1: Clean raw text data
    print("\n1. Cleaning raw text data...")
    raw_data = clean_raw_text_data(lariat_txt)
    entities = raw_data['entities']

    # Step 2: Load research data
    print("\n2. Loading research data...")
    research_data = load_research_data()

    # Step 3: Enrich entities with research intersections
    print("\n3. Enriching entities with research data...")
    enriched_entities = enrich_entities_with_research(entities, research_data)

    # Step 4: Calculate data quality
    print("\n4. Calculating data quality metrics...")
    quality_report = calculate_data_quality(enriched_entities)

    # Step 5: Create relationship graph
    print("\n5. Creating entity relationship graph...")
    relationship_graph = create_entity_relationship_graph(enriched_entities)

    # Step 6: Save processed data
    print("\n6. Saving processed data...")

    # Save cleaned entities
    cleaned_file = DATA_PROCESSED_DIR / "lariat_entities_cleaned.json"
    with open(cleaned_file, 'w') as f:
        json.dump({'entities': entities, 'metadata': {'generated': datetime.now().isoformat()}}, f, indent=2)
    print(f"  Saved cleaned entities to: {cleaned_file}")

    # Save enriched entities
    enriched_file = DATA_PROCESSED_DIR / "lariat_enriched.json"
    with open(enriched_file, 'w') as f:
        json.dump({
            'entities': enriched_entities,
            'metadata': {
                'generated': datetime.now().isoformat(),
                'source': 'preprocess_violation_data.py',
                'research_intersections': True
            }
        }, f, indent=2)
    print(f"  Saved enriched entities to: {enriched_file}")

    # Save relationship graph
    graph_file = DATA_PROCESSED_DIR / "entity_relationships.json"
    with open(graph_file, 'w') as f:
        json.dump({
            'graph': relationship_graph,
            'metadata': {
                'generated': datetime.now().isoformat(),
                'node_count': len(relationship_graph['nodes']),
                'edge_count': len(relationship_graph['edges'])
            }
        }, f, indent=2)
    print(f"  Saved relationship graph to: {graph_file}")

    # Save quality report
    quality_file = DATA_PROCESSED_DIR / "data_quality_report.json"
    with open(quality_file, 'w') as f:
        json.dump({
            'quality_metrics': quality_report,
            'metadata': {
                'generated': datetime.now().isoformat(),
                'analyzed_entities': len(enriched_entities)
            }
        }, f, indent=2)
    print(f"  Saved quality report to: {quality_file}")

    print("\n" + "=" * 60)
    print("Preprocessing complete!")
    print(f"  Processed {len(enriched_entities)} entities")
    print(f"  Quality score: {quality_report.get('overall_score', {}).get('completeness', 0):.1f}%")
    print("=" * 60)


if __name__ == '__main__':
    main()
