#!/usr/bin/env python3
"""
Process lariat.txt file containing Texas business filings
Converts to structured JSON and generates embeddings
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "sentence-transformers"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Warning: Could not install sentence-transformers automatically.")
        print("Please install manually: pip install --user sentence-transformers")
        sys.exit(1)
    from sentence_transformers import SentenceTransformer

def parse_lariat_file(file_path: Path) -> Dict[str, Any]:
    """Parse lariat.txt file and extract all entity filings"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use a dictionary to consolidate entities by filing number
    entities_dict = {}
    current_filing_number = None
    current_entity = None
    current_section = None

    lines = content.split('\n')

    for i, line in enumerate(lines):
        line = line.rstrip()

        # Detect new entity filing
        if 'Filing Number:' in line:
            # Extract filing number
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                filing_num = match.group(1)

                # If we already have this entity, use it; otherwise create new
                if filing_num in entities_dict:
                    current_entity = entities_dict[filing_num]
                    current_filing_number = filing_num
                else:
                    current_entity = {
                        'filing_number': filing_num,
                        'entity_type': None,
                        'original_date_of_filing': None,
                        'entity_status': None,
                        'formation_date': None,
                        'tax_id': None,
                        'fein': None,
                        'duration': None,
                        'name': None,
                        'address': None,
                        'jurisdiction': None,
                        'foreign_formation_date': None,
                        'fictitious_name': None,
                        'registered_agent': None,
                        'filing_history': [],
                        'names': [],
                        'management': [],
                        'assumed_names': [],
                        'associated_entities': [],
                        'initial_address': None
                    }
                    entities_dict[filing_num] = current_entity
                    current_filing_number = filing_num

                current_section = 'header'

                # Parse entity_type from same line if present
                entity_type_match = re.search(r'Entity Type:\s+([^\t\n]+)', line)
                if entity_type_match:
                    current_entity['entity_type'] = entity_type_match.group(1).strip()

        elif current_entity:
            # Parse entity type (may be on same line as Filing Number)
            elif 'Entity Type:' in line:
                match = re.search(r'Entity Type:\s+([^\t\n]+)', line)
                if match:
                    current_entity['entity_type'] = match.group(1).strip()

            # Parse original date of filing (may be on same line as Entity Status)
            if 'Original Date of Filing:' in line:
                match = re.search(r'Original Date of Filing:\s+([^\t]+)', line)
                if match:
                    current_entity['original_date_of_filing'] = match.group(1).strip()
                # Also parse entity_status from same line if present
                status_match = re.search(r'Entity Status:\s+([^\t\n]+)', line)
                if status_match:
                    current_entity['entity_status'] = status_match.group(1).strip()

            # Parse entity status (may be on same line as Original Date of Filing)
            elif 'Entity Status:' in line:
                match = re.search(r'Entity Status:\s+([^\t\n]+)', line)
                if match:
                    current_entity['entity_status'] = match.group(1).strip()

            # Parse formation date
            elif 'Formation Date:' in line:
                match = re.search(r'Formation Date:\s+(.+)', line)
                if match:
                    value = match.group(1).strip()
                    current_entity['formation_date'] = None if value == 'N/A' else value

            # Parse Tax ID
            elif 'Tax ID:' in line:
                match = re.search(r'Tax ID:\s+(\d+)', line)
                if match:
                    current_entity['tax_id'] = match.group(1)

            # Parse FEIN
            elif 'FEIN:' in line:
                match = re.search(r'FEIN:\s+(\d+)', line)
                if match:
                    current_entity['fein'] = match.group(1)

            # Parse Duration
            elif 'Duration:' in line:
                match = re.search(r'Duration:\s+(.+)', line)
                if match:
                    current_entity['duration'] = match.group(1).strip()

            # Parse Name
            elif line.startswith('Name:'):
                match = re.search(r'Name:\s+(.+)', line)
                if match:
                    current_entity['name'] = match.group(1).strip()

            # Parse Address (multi-line)
            elif line.startswith('Address:'):
                match = re.search(r'Address:\s+(.+)', line)
                if match:
                    address_parts = [match.group(1).strip()]
                    # Check next lines for address continuation
                    j = i + 1
                    while j < len(lines) and j < i + 5:  # Limit to 5 lines
                        addr_line = lines[j].strip()
                        if not addr_line:
                            break
                        if addr_line.startswith('REGISTERED AGENT') or addr_line.startswith('Filing Number:'):
                            break
                        if addr_line and not addr_line.startswith('REGISTERED') and not addr_line.startswith('FILING'):
                            address_parts.append(addr_line)
                        j += 1
                    current_entity['address'] = '\n'.join(address_parts)

            # Parse Jurisdiction (for foreign entities)
            elif 'Jurisdiction:' in line:
                match = re.search(r'Jurisdiction:\s+(.+)', line)
                if match:
                    current_entity['jurisdiction'] = match.group(1).strip()

            # Parse Foreign Formation Date
            elif 'Foreign Formation Date:' in line:
                match = re.search(r'Foreign Formation Date:\s+(.+)', line)
                if match:
                    current_entity['foreign_formation_date'] = match.group(1).strip()

            # Parse Fictitious Name
            elif 'Fictitious Name:' in line:
                match = re.search(r'Fictitious Name:\s+(.+)', line)
                if match:
                    value = match.group(1).strip()
                    current_entity['fictitious_name'] = None if value == 'N/A' else value

            # Detect section headers
            elif 'REGISTERED AGENT' in line:
                if 'FILING HISTORY' in line or 'NAMES' in line or 'MANAGEMENT' in line:
                    # This is a header row with multiple sections
                    current_section = 'registered_agent'
                elif line.strip() == 'REGISTERED AGENT' or (line.strip().startswith('Name') and 'Address' in line):
                    current_section = 'registered_agent'

            elif 'FILING HISTORY' in line or line.strip().startswith('View Image') or line.strip().startswith('Document Number'):
                current_section = 'filing_history'

            elif 'NAMES' in line or (line.strip().startswith('Name') and 'Name Status' in line and 'Name Type' in line):
                current_section = 'names'

            elif 'MANAGEMENT' in line or (line.strip().startswith('Last Update') and 'Name' in line and 'Title' in line):
                current_section = 'management'

            elif 'ASSUMED NAMES' in line or (line.strip().startswith('Assumed Name') and 'Date of Filing' in line):
                current_section = 'assumed_names'

            elif 'ASSOCIATED ENTITIES' in line or (line.strip().startswith('Name') and 'Entity Type' in line and 'Document Description' in line):
                current_section = 'associated_entities'

            elif 'INITIAL ADDRESS' in line or (line.strip() == 'Address' and current_section == 'initial_address'):
                current_section = 'initial_address'

            # Parse registered agent
            elif current_section == 'registered_agent' and line.strip() and not line.startswith('REGISTERED AGENT') and not line.startswith('Name') and 'Address' not in line:
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 1:
                    agent_name = parts[0]
                    # Skip if it's a header row
                    if agent_name and agent_name != 'Name' and agent_name.lower() != 'address':
                        agent_address = parts[1] if len(parts) > 1 else ''
                        # Handle multi-line addresses
                        if not agent_address and i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line and not next_line.startswith('Filing Number') and not next_line.startswith('REGISTERED'):
                                agent_address = next_line
                                if i + 2 < len(lines):
                                    next_next = lines[i + 2].strip()
                                    if next_next and not next_next.startswith('Filing Number') and not next_next.startswith('REGISTERED'):
                                        agent_address += '\n' + next_next

                        inactive_date = parts[2] if len(parts) > 2 else None

                        if not current_entity.get('registered_agent') or isinstance(current_entity['registered_agent'], str):
                            current_entity['registered_agent'] = {
                                'name': agent_name,
                                'address': agent_address,
                                'inactive_date': inactive_date
                            }

            # Parse filing history
            elif current_section == 'filing_history' and line.strip() and not line.startswith('View Image') and not line.startswith('Document Number'):
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 3:
                    # Handle case where first part might be empty (leading tab)
                    doc_num_idx = 0 if parts[0] else 1
                    filing = {
                        'document_number': parts[doc_num_idx] if doc_num_idx < len(parts) else None,
                        'filing_type': parts[doc_num_idx + 1] if doc_num_idx + 1 < len(parts) else None,
                        'filing_date': parts[doc_num_idx + 2] if doc_num_idx + 2 < len(parts) else None,
                        'effective_date': parts[doc_num_idx + 3] if doc_num_idx + 3 < len(parts) else None,
                        'eff_cond': parts[doc_num_idx + 4] if doc_num_idx + 4 < len(parts) else None,
                        'page_count': parts[doc_num_idx + 5] if doc_num_idx + 5 < len(parts) else None
                    }
                    # Check if this filing already exists
                    existing = [f for f in current_entity['filing_history']
                               if f.get('document_number') == filing.get('document_number')]
                    if not existing:
                        current_entity['filing_history'].append(filing)

            # Parse names
            elif current_section == 'names' and line.strip() and not line.startswith('Name') and not line.startswith('Name Status'):
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 2:
                    name_entry = {
                        'name': parts[0] if len(parts) > 0 else None,
                        'name_status': parts[1] if len(parts) > 1 else None,
                        'name_type': parts[2] if len(parts) > 2 else None,
                        'name_inactive_date': parts[3] if len(parts) > 3 else None,
                        'consent_filing_number': parts[4] if len(parts) > 4 else None
                    }
                    # Check if this name entry already exists
                    existing = [n for n in current_entity['names']
                              if n.get('name') == name_entry.get('name') and
                                 n.get('name_status') == name_entry.get('name_status')]
                    if not existing:
                        current_entity['names'].append(name_entry)

            # Parse management
            elif current_section == 'management' and line.strip() and not line.startswith('Last Update') and not line.startswith('Name') and 'Title' not in line:
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 2:
                    mgmt_entry = {
                        'last_update': parts[0] if len(parts) > 0 else None,
                        'name': parts[1] if len(parts) > 1 else None,
                        'title': parts[2] if len(parts) > 2 else None,
                        'address': None
                    }
                    # Handle multi-line addresses - check next lines
                    if len(parts) >= 4:
                        mgmt_entry['address'] = parts[3]
                    elif i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('Filing Number') and not next_line.startswith('Last Update') and not next_line.startswith('REGISTERED'):
                            mgmt_entry['address'] = next_line
                            if i + 2 < len(lines):
                                next_next = lines[i + 2].strip()
                                if next_next and not next_next.startswith('Filing Number') and not next_next.startswith('Last Update') and not next_next.startswith('REGISTERED'):
                                    mgmt_entry['address'] += '\n' + next_next

                    # Only add if we have a name
                    if mgmt_entry.get('name'):
                        # Check if this entry already exists
                        existing = [m for m in current_entity['management']
                                  if m.get('name') == mgmt_entry.get('name') and
                                     m.get('title') == mgmt_entry.get('title')]
                        if not existing:
                            current_entity['management'].append(mgmt_entry)

            # Parse assumed names
            elif current_section == 'assumed_names' and line.strip() and not line.startswith('Assumed Name'):
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 3:
                    assumed_name = {
                        'assumed_name': parts[0] if len(parts) > 0 else None,
                        'date_of_filing': parts[1] if len(parts) > 1 else None,
                        'expiration_date': parts[2] if len(parts) > 2 else None,
                        'inactive_date': parts[3] if len(parts) > 3 else None,
                        'name_status': parts[4] if len(parts) > 4 else None,
                        'counties': parts[5] if len(parts) > 5 else None
                    }
                    current_entity['assumed_names'].append(assumed_name)

            # Parse associated entities
            elif current_section == 'associated_entities' and line.strip() and not line.startswith('Name') and not line.startswith('Entity Type'):
                parts = [p.strip() for p in line.split('\t') if p.strip()]
                if len(parts) >= 3:
                    associated = {
                        'name': parts[0] if len(parts) > 0 else None,
                        'entity_type': parts[1] if len(parts) > 1 else None,
                        'document_description': parts[2] if len(parts) > 2 else None,
                        'filing_date': parts[3] if len(parts) > 3 else None,
                        'entity_filing_number': parts[4] if len(parts) > 4 else None,
                        'jurisdiction': parts[5] if len(parts) > 5 else None,
                        'capacity': parts[6] if len(parts) > 6 else None
                    }
                    current_entity['associated_entities'].append(associated)

            # Parse initial address
            elif current_section == 'initial_address' and line.strip() and not line.startswith('Address'):
                if not current_entity['initial_address']:
                    current_entity['initial_address'] = line.strip()
                else:
                    current_entity['initial_address'] += '\n' + line.strip()

    # Convert dict to list
    entities = list(entities_dict.values())

    return {
        'metadata': {
            'source_file': str(file_path),
            'processing_date': datetime.now().isoformat(),
            'state': 'Texas',
            'total_entities': len(entities)
        },
        'entities': entities
    }

def create_text_representations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create text representations for embedding"""
    texts = []

    for entity in data.get('entities', []):
        # Create comprehensive text representation
        text_parts = []

        if entity.get('filing_number'):
            text_parts.append(f"Filing Number: {entity['filing_number']}")
        if entity.get('name'):
            text_parts.append(f"Name: {entity['name']}")
        if entity.get('entity_type'):
            text_parts.append(f"Entity Type: {entity['entity_type']}")
        if entity.get('entity_status'):
            text_parts.append(f"Status: {entity['entity_status']}")
        if entity.get('address'):
            text_parts.append(f"Address: {entity['address']}")
        if entity.get('registered_agent'):
            agent = entity['registered_agent']
            if isinstance(agent, dict):
                text_parts.append(f"Registered Agent: {agent.get('name', '')} - {agent.get('address', '')}")
            else:
                text_parts.append(f"Registered Agent: {agent}")
        if entity.get('tax_id'):
            text_parts.append(f"Tax ID: {entity['tax_id']}")
        if entity.get('fein'):
            text_parts.append(f"FEIN: {entity['fein']}")
        if entity.get('jurisdiction'):
            text_parts.append(f"Jurisdiction: {entity['jurisdiction']}")
        if entity.get('formation_date'):
            text_parts.append(f"Formation Date: {entity['formation_date']}")
        if entity.get('original_date_of_filing'):
            text_parts.append(f"Original Filing Date: {entity['original_date_of_filing']}")

        # Add management information
        if entity.get('management'):
            mgmt_text = "Management: " + "; ".join([
                f"{m.get('name', '')} ({m.get('title', '')})"
                for m in entity['management']
                if m.get('name')
            ])
            text_parts.append(mgmt_text)

        # Add filing history summary
        if entity.get('filing_history'):
            filing_summary = "Filing History: " + "; ".join([
                f"{f.get('filing_type', '')} on {f.get('filing_date', '')}"
                for f in entity['filing_history'][:5]  # Limit to first 5
            ])
            text_parts.append(filing_summary)

        full_text = " | ".join(text_parts)

        texts.append({
            'filing_number': entity.get('filing_number'),
            'entity_name': entity.get('name'),
            'text': full_text,
            'metadata': entity
        })

    return texts

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """Generate embeddings for texts"""
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print(f"Generating embeddings for {len(texts)} texts...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    return embeddings

def main():
    """Main function"""
    print("=" * 70)
    print("Lariat Texas Filings - JSON Conversion and Embedding Generation")
    print("=" * 70)

    # Input file
    input_file = PROJECT_ROOT / "data" / "raw" / "lariat.txt"
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Parse file
    print("\n1. Parsing lariat.txt file...")
    data = parse_lariat_file(input_file)
    print(f"   ✓ Parsed {len(data['entities'])} entities")

    # Create text representations
    print("\n2. Creating text representations...")
    texts = create_text_representations(data)
    print(f"   ✓ Created {len(texts)} text representations")

    # Generate embeddings
    print("\n3. Generating embeddings...")
    text_strings = [t['text'] for t in texts]
    embeddings = generate_embeddings(text_strings)
    print(f"   ✓ Generated embeddings (shape: {embeddings.shape})")

    # Add embeddings to text representations
    for i, text_rep in enumerate(texts):
        text_rep['embedding'] = embeddings[i].tolist()

    # Save JSON output
    output_json = PROJECT_ROOT / "research" / "company_registrations" / "data" / "texas" / "lariat_tx_filings.json"
    output_json.parent.mkdir(parents=True, exist_ok=True)

    json_output = {
        'metadata': {
            **data['metadata'],
            'embedding_model': 'all-MiniLM-L6-v2',
            'embedding_dimension': embeddings.shape[1] if len(embeddings.shape) > 1 else len(embeddings),
            'total_embeddings': len(embeddings)
        },
        'entities': data['entities'],
        'embeddings': [
            {
                'filing_number': t['filing_number'],
                'entity_name': t['entity_name'],
                'text': t['text'],
                'embedding': t['embedding']
            }
            for t in texts
        ]
    }

    print(f"\n4. Saving JSON output to {output_json}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)
    print(f"   ✓ JSON saved")

    # Save embeddings separately for vector database
    embeddings_output = PROJECT_ROOT / "data" / "vectors" / "lariat_tx_embeddings.json"
    embeddings_output.parent.mkdir(parents=True, exist_ok=True)

    embeddings_data = {
        'metadata': {
            'source': 'lariat.txt',
            'state': 'Texas',
            'model': 'all-MiniLM-L6-v2',
            'dimension': embeddings.shape[1] if len(embeddings.shape) > 1 else len(embeddings),
            'count': len(embeddings),
            'created': datetime.now().isoformat()
        },
        'vectors': [
            {
                'id': f"lariat_tx_{texts[i]['filing_number']}",
                'text': texts[i]['text'],
                'embedding': embeddings[i].tolist(),
                'metadata': {
                    'filing_number': texts[i]['filing_number'],
                    'entity_name': texts[i]['entity_name'],
                    'entity_type': texts[i]['metadata'].get('entity_type'),
                    'entity_status': texts[i]['metadata'].get('entity_status'),
                    'address': texts[i]['metadata'].get('address')
                }
            }
            for i in range(len(texts))
        ]
    }

    print(f"\n5. Saving embeddings to {embeddings_output}")
    with open(embeddings_output, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Embeddings saved")

    print("\n" + "=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total entities processed: {len(data['entities'])}")
    print(f"Embeddings generated: {len(embeddings)}")
    print(f"Embedding dimension: {embeddings.shape[1] if len(embeddings.shape) > 1 else len(embeddings)}")
    print(f"\nJSON output: {output_json}")
    print(f"Embeddings output: {embeddings_output}")
    print("\n" + "=" * 70)
    print("Processing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
