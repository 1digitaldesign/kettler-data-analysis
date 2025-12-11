#!/usr/bin/env python3
"""
Recursively break down lariat TX filings by JSON keys
Creates separate JSON files and embeddings for each recursive structure
"""

import json
import sys
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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "sentence-transformers"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Warning: Could not install sentence-transformers automatically.")
        sys.exit(1)
    from sentence_transformers import SentenceTransformer

def create_text_representation(data: Dict[str, Any], prefix: str = "") -> str:
    """Create text representation for embedding"""
    text_parts = []

    if isinstance(data, dict):
        for key, value in data.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    if isinstance(value, list) and len(value) > 0:
                        text_parts.append(f"{key}: {len(value)} items")
                    elif isinstance(value, dict):
                        text_parts.append(f"{key}: {json.dumps(value, separators=(',', ':'))}")
                else:
                    text_parts.append(f"{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                text_parts.append(f"Item {i}: {json.dumps(item, separators=(',', ':'))}")
            else:
                text_parts.append(f"Item {i}: {item}")
    else:
        text_parts.append(str(data))

    return " | ".join(text_parts)

def generate_embedding(text: str, model: SentenceTransformer) -> List[float]:
    """Generate embedding for text"""
    if not text or not text.strip():
        return None
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def save_json_with_embedding(data: Dict[str, Any], file_path: Path, model: SentenceTransformer,
                            text_representation: Optional[str] = None):
    """Save JSON file and generate embedding"""
    # Create directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate text representation if not provided
    if text_representation is None:
        text_representation = create_text_representation(data)

    # Generate embedding
    embedding = generate_embedding(text_representation, model)

    # Create output structure
    output = {
        'metadata': {
            'source': 'lariat_tx_filings',
            'created': datetime.now().isoformat(),
            'file_path': str(file_path),
            'has_embedding': embedding is not None
        },
        'data': data,
        'text_representation': text_representation,
        'embedding': embedding
    }

    # Save JSON
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return output

def process_entity(entity: Dict[str, Any], base_dir: Path, model: SentenceTransformer,
                  index: Dict[str, Any]):
    """Process a single entity recursively"""
    filing_number = entity.get('filing_number', 'unknown')

    # 1. Save entity-level JSON
    entity_dir = base_dir / 'entities'
    entity_file = entity_dir / f"entity_{filing_number}.json"
    entity_text = create_text_representation(entity, prefix=f"Entity {filing_number}")
    save_json_with_embedding(entity, entity_file, model, entity_text)
    index['entities'].append({
        'filing_number': filing_number,
        'file': str(entity_file.relative_to(PROJECT_ROOT)),
        'name': entity.get('name'),
        'entity_type': entity.get('entity_type')
    })

    # 2. Process registered_agent
    if entity.get('registered_agent'):
        agent = entity['registered_agent']
        if isinstance(agent, dict):
            agent_dir = base_dir / 'registered_agents'
            agent_file = agent_dir / f"registered_agent_{filing_number}.json"
            agent_text = create_text_representation(agent, prefix=f"Registered Agent for {filing_number}")
            save_json_with_embedding(agent, agent_file, model, agent_text)
            index['registered_agents'].append({
                'filing_number': filing_number,
                'file': str(agent_file.relative_to(PROJECT_ROOT)),
                'agent_name': agent.get('name')
            })

    # 3. Process filing_history (array)
    if entity.get('filing_history'):
        for i, filing in enumerate(entity['filing_history']):
            filing_dir = base_dir / 'filing_history'
            doc_number = filing.get('document_number', f'{filing_number}_{i}')
            filing_file = filing_dir / f"filing_{doc_number}.json"
            filing_text = create_text_representation(filing, prefix=f"Filing {doc_number}")
            save_json_with_embedding(filing, filing_file, model, filing_text)
            index['filing_history'].append({
                'filing_number': filing_number,
                'document_number': doc_number,
                'file': str(filing_file.relative_to(PROJECT_ROOT)),
                'filing_type': filing.get('filing_type'),
                'filing_date': filing.get('filing_date')
            })

    # 4. Process names (array)
    if entity.get('names'):
        for i, name_entry in enumerate(entity['names']):
            names_dir = base_dir / 'names'
            name_file = names_dir / f"name_{filing_number}_{i}.json"
            name_text = create_text_representation(name_entry, prefix=f"Name entry {i} for {filing_number}")
            save_json_with_embedding(name_entry, name_file, model, name_text)
            index['names'].append({
                'filing_number': filing_number,
                'index': i,
                'file': str(name_file.relative_to(PROJECT_ROOT)),
                'name': name_entry.get('name'),
                'name_status': name_entry.get('name_status')
            })

    # 5. Process management (array)
    if entity.get('management'):
        for i, mgmt_entry in enumerate(entity['management']):
            mgmt_dir = base_dir / 'management'
            mgmt_file = mgmt_dir / f"management_{filing_number}_{i}.json"
            mgmt_text = create_text_representation(mgmt_entry, prefix=f"Management entry {i} for {filing_number}")
            save_json_with_embedding(mgmt_entry, mgmt_file, model, mgmt_text)
            index['management'].append({
                'filing_number': filing_number,
                'index': i,
                'file': str(mgmt_file.relative_to(PROJECT_ROOT)),
                'name': mgmt_entry.get('name'),
                'title': mgmt_entry.get('title')
            })

    # 6. Process assumed_names (array)
    if entity.get('assumed_names'):
        for i, assumed_name in enumerate(entity['assumed_names']):
            assumed_dir = base_dir / 'assumed_names'
            assumed_file = assumed_dir / f"assumed_name_{filing_number}_{i}.json"
            assumed_text = create_text_representation(assumed_name, prefix=f"Assumed name {i} for {filing_number}")
            save_json_with_embedding(assumed_name, assumed_file, model, assumed_text)
            index['assumed_names'].append({
                'filing_number': filing_number,
                'index': i,
                'file': str(assumed_file.relative_to(PROJECT_ROOT)),
                'assumed_name': assumed_name.get('assumed_name')
            })

    # 7. Process associated_entities (array)
    if entity.get('associated_entities'):
        for i, associated in enumerate(entity['associated_entities']):
            associated_dir = base_dir / 'associated_entities'
            associated_file = associated_dir / f"associated_entity_{filing_number}_{i}.json"
            associated_text = create_text_representation(associated, prefix=f"Associated entity {i} for {filing_number}")
            save_json_with_embedding(associated, associated_file, model, associated_text)
            index['associated_entities'].append({
                'filing_number': filing_number,
                'index': i,
                'file': str(associated_file.relative_to(PROJECT_ROOT)),
                'name': associated.get('name'),
                'entity_type': associated.get('entity_type')
            })

    # 8. Process initial_address (if exists)
    if entity.get('initial_address'):
        address_dir = base_dir / 'initial_addresses'
        address_file = address_dir / f"initial_address_{filing_number}.json"
        address_data = {'filing_number': filing_number, 'address': entity['initial_address']}
        address_text = create_text_representation(address_data, prefix=f"Initial address for {filing_number}")
        save_json_with_embedding(address_data, address_file, model, address_text)
        index['initial_addresses'].append({
            'filing_number': filing_number,
            'file': str(address_file.relative_to(PROJECT_ROOT)),
            'address': entity['initial_address']
        })

def main():
    """Main function"""
    print("=" * 70)
    print("Recursive Lariat TX Filings Breakdown")
    print("=" * 70)

    # Load source data
    source_file = PROJECT_ROOT / "research" / "company_registrations" / "data" / "texas" / "lariat_tx_filings.json"
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    print(f"\n1. Loading source data from {source_file}")
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    entities = source_data.get('entities', [])
    print(f"   ✓ Loaded {len(entities)} entities")

    # Initialize embedding model
    print("\n2. Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   ✓ Model loaded (dimension: {model.get_sentence_embedding_dimension()})")

    # Create base directory
    base_dir = PROJECT_ROOT / "research" / "texas" / "lariat"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Initialize index
    index = {
        'metadata': {
            'source': 'lariat_tx_filings',
            'created': datetime.now().isoformat(),
            'total_entities': len(entities),
            'embedding_model': 'all-MiniLM-L6-v2',
            'embedding_dimension': model.get_sentence_embedding_dimension()
        },
        'entities': [],
        'registered_agents': [],
        'filing_history': [],
        'names': [],
        'management': [],
        'assumed_names': [],
        'associated_entities': [],
        'initial_addresses': []
    }

    # Process each entity recursively
    print("\n3. Processing entities recursively...")
    for i, entity in enumerate(entities):
        filing_number = entity.get('filing_number', f'unknown_{i}')
        print(f"   Processing entity {i+1}/{len(entities)}: {filing_number}")
        process_entity(entity, base_dir, model, index)

    # Save index
    index_file = base_dir / "index.json"
    print(f"\n4. Saving index to {index_file}")
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Index saved")

    # Print summary
    print("\n" + "=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total entities: {len(index['entities'])}")
    print(f"Registered agents: {len(index['registered_agents'])}")
    print(f"Filing history items: {len(index['filing_history'])}")
    print(f"Names entries: {len(index['names'])}")
    print(f"Management entries: {len(index['management'])}")
    print(f"Assumed names: {len(index['assumed_names'])}")
    print(f"Associated entities: {len(index['associated_entities'])}")
    print(f"Initial addresses: {len(index['initial_addresses'])}")
    print(f"\nBase directory: {base_dir}")
    print(f"Index file: {index_file}")
    print("\n" + "=" * 70)
    print("Processing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
