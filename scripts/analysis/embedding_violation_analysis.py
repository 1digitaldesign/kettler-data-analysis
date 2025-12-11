#!/usr/bin/env python3
"""
Embedding-based similarity analysis for violation patterns
Uses cosine similarity to find entities with similar violation patterns
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_VECTORS_DIR, DATA_PROCESSED_DIR


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def extract_entity_info(text: str) -> Dict[str, str]:
    """Extract entity information from embedding text"""
    info = {}

    # Extract filing number
    filing_match = text.find('Filing Number:')
    if filing_match != -1:
        parts = text[filing_match:].split('|')
        for part in parts:
            if 'Filing Number:' in part:
                match = part.split('Filing Number:')[1].strip().split()[0]
                info['filing_number'] = match

    # Extract name
    name_match = text.find('Name:')
    if name_match != -1:
        parts = text[name_match:].split('|')
        for part in parts:
            if 'Name:' in part:
                name = part.split('Name:')[1].strip().split('|')[0].strip()
                info['name'] = name

    # Extract address
    addr_match = text.find('Address:')
    if addr_match != -1:
        parts = text[addr_match:].split('|')
        for part in parts:
            if 'Address:' in part:
                addr = part.split('Address:')[1].strip().split('|')[0].strip()
                info['address'] = addr.replace('\n', ' ')

    # Extract status
    status_match = text.find('Status:')
    if status_match != -1:
        parts = text[status_match:].split('|')
        for part in parts:
            if 'Status:' in part:
                status = part.split('Status:')[1].strip().split('|')[0].strip()
                info['status'] = status

    # Extract registered agent
    agent_match = text.find('Registered Agent:')
    if agent_match != -1:
        parts = text[agent_match:].split('|')
        for part in parts:
            if 'Registered Agent:' in part:
                agent = part.split('Registered Agent:')[1].strip().split('|')[0].strip()
                info['registered_agent'] = agent

    # Extract Tax ID
    tax_match = text.find('Tax ID:')
    if tax_match != -1:
        parts = text[tax_match:].split('|')
        for part in parts:
            if 'Tax ID:' in part:
                tax_id = part.split('Tax ID:')[1].strip().split()[0]
                info['tax_id'] = tax_id

    # Check for violations in text
    if 'Tax Forfeiture' in text:
        info['has_tax_forfeiture'] = True
    if 'Forfeited' in text:
        info['has_forfeited_status'] = True
    if 'Reinstatement' in text:
        info['has_reinstatement'] = True

    return info


def find_similar_entities(embeddings_data: Dict[str, Any],
                         similarity_threshold: float = 0.7) -> Dict[str, Any]:
    """Find entities with similar violation patterns using cosine similarity"""
    vectors = embeddings_data.get('vectors', [])

    if len(vectors) < 2:
        return {'similarity_pairs': [], 'clusters': []}

    # Build similarity matrix
    similarity_pairs = []
    entity_embeddings = {}
    entity_info = {}

    for vec in vectors:
        entity_id = vec.get('id', '').replace('lariat_tx_', '')
        embedding = vec.get('embedding', [])
        text = vec.get('text', '')

        if embedding and len(embedding) > 0:
            entity_embeddings[entity_id] = embedding
            entity_info[entity_id] = extract_entity_info(text)
            entity_info[entity_id]['original_id'] = vec.get('id', '')

    # Calculate pairwise similarities
    entity_ids = list(entity_embeddings.keys())
    for i, entity_id1 in enumerate(entity_ids):
        for entity_id2 in entity_ids[i+1:]:
            similarity = cosine_similarity(
                entity_embeddings[entity_id1],
                entity_embeddings[entity_id2]
            )

            if similarity >= similarity_threshold:
                similarity_pairs.append({
                    'entity1': entity_id1,
                    'entity2': entity_id2,
                    'similarity': similarity,
                    'entity1_info': entity_info[entity_id1],
                    'entity2_info': entity_info[entity_id2]
                })

    # Sort by similarity
    similarity_pairs.sort(key=lambda x: x['similarity'], reverse=True)

    return {
        'similarity_pairs': similarity_pairs,
        'entity_info': entity_info,
        'threshold': similarity_threshold
    }


def find_address_clusters(entity_info: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Find entities sharing addresses (potential shell companies)"""
    address_to_entities = defaultdict(list)

    for entity_id, info in entity_info.items():
        address = info.get('address', '').upper()
        if address:
            address_to_entities[address].append({
                'entity_id': entity_id,
                'name': info.get('name'),
                'filing_number': info.get('filing_number')
            })

    clusters = []
    for address, entities in address_to_entities.items():
        if len(entities) > 1:
            clusters.append({
                'address': address,
                'entity_count': len(entities),
                'entities': entities,
                'cluster_type': 'address'
            })

    return clusters


def find_agent_clusters(entity_info: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Find entities sharing registered agents"""
    agent_to_entities = defaultdict(list)

    for entity_id, info in entity_info.items():
        agent = info.get('registered_agent', '').upper()
        if agent:
            agent_to_entities[agent].append({
                'entity_id': entity_id,
                'name': info.get('name'),
                'filing_number': info.get('filing_number')
            })

    clusters = []
    for agent, entities in agent_to_entities.items():
        if len(entities) > 1:
            clusters.append({
                'agent': agent,
                'entity_count': len(entities),
                'entities': entities,
                'cluster_type': 'registered_agent'
            })

    return clusters


def find_violation_pattern_clusters(entity_info: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Find entities with similar violation patterns"""
    violation_patterns = defaultdict(list)

    for entity_id, info in entity_info.items():
        pattern_key = []

        if info.get('has_tax_forfeiture'):
            pattern_key.append('tax_forfeiture')
        if info.get('has_forfeited_status'):
            pattern_key.append('forfeited_status')
        if info.get('has_reinstatement'):
            pattern_key.append('reinstatement')

        pattern_str = '_'.join(sorted(pattern_key)) if pattern_key else 'no_violations'

        violation_patterns[pattern_str].append({
            'entity_id': entity_id,
            'name': info.get('name'),
            'filing_number': info.get('filing_number'),
            'pattern': pattern_key
        })

    clusters = []
    for pattern, entities in violation_patterns.items():
        if len(entities) > 1:
            clusters.append({
                'pattern': pattern,
                'entity_count': len(entities),
                'entities': entities,
                'cluster_type': 'violation_pattern'
            })

    return clusters


def create_violation_clusters(similarity_results: Dict[str, Any],
                             entity_info: Dict[str, Dict]) -> List[Dict[str, Any]]:
    """Create violation clusters based on similarity and patterns"""
    clusters = []

    # Address-based clusters
    address_clusters = find_address_clusters(entity_info)
    clusters.extend(address_clusters)

    # Agent-based clusters
    agent_clusters = find_agent_clusters(entity_info)
    clusters.extend(agent_clusters)

    # Violation pattern clusters
    pattern_clusters = find_violation_pattern_clusters(entity_info)
    clusters.extend(pattern_clusters)

    # High similarity clusters
    similarity_pairs = similarity_results.get('similarity_pairs', [])
    high_similarity = [p for p in similarity_pairs if p['similarity'] >= 0.85]

    if high_similarity:
        clusters.append({
            'cluster_type': 'high_similarity',
            'entity_count': len(high_similarity) * 2,  # Each pair has 2 entities
            'similarity_pairs': high_similarity[:10],  # Top 10
            'description': 'Entities with very high embedding similarity (>=0.85)'
        })

    return clusters


def main():
    """Main embedding analysis function"""
    print("=" * 60)
    print("Embedding-Based Violation Analysis")
    print("=" * 60)

    # Load embeddings
    embeddings_file = DATA_VECTORS_DIR / "lariat_tx_embeddings.json"
    if not embeddings_file.exists():
        print(f"Error: {embeddings_file} not found")
        return

    print(f"\n1. Loading embeddings from: {embeddings_file}")
    with open(embeddings_file, 'r') as f:
        embeddings_data = json.load(f)

    vector_count = len(embeddings_data.get('vectors', []))
    print(f"   Loaded {vector_count} entity embeddings")

    # Find similar entities
    print("\n2. Calculating similarity scores...")
    similarity_results = find_similar_entities(embeddings_data, similarity_threshold=0.7)
    similarity_pairs = similarity_results.get('similarity_pairs', [])
    entity_info = similarity_results.get('entity_info', {})

    print(f"   Found {len(similarity_pairs)} entity pairs with similarity >= 0.7")

    if similarity_pairs:
        print(f"   Highest similarity: {similarity_pairs[0]['similarity']:.3f}")
        print(f"   Between: {similarity_pairs[0]['entity1_info'].get('name')} and {similarity_pairs[0]['entity2_info'].get('name')}")

    # Create violation clusters
    print("\n3. Creating violation clusters...")
    clusters = create_violation_clusters(similarity_results, entity_info)

    address_clusters = [c for c in clusters if c['cluster_type'] == 'address']
    agent_clusters = [c for c in clusters if c['cluster_type'] == 'registered_agent']
    pattern_clusters = [c for c in clusters if c['cluster_type'] == 'violation_pattern']

    print(f"   Address clusters: {len(address_clusters)}")
    print(f"   Agent clusters: {len(agent_clusters)}")
    print(f"   Violation pattern clusters: {len(pattern_clusters)}")

    # Identify entities for investigation
    print("\n4. Identifying entities for investigation...")
    investigation_candidates = []

    # Entities in multiple clusters
    entity_cluster_count = defaultdict(int)
    for cluster in clusters:
        if 'entities' in cluster:
            for entity in cluster['entities']:
                entity_id = entity.get('entity_id') or entity.get('filing_number')
                if entity_id:
                    entity_cluster_count[entity_id] += 1

    high_risk_entities = [eid for eid, count in entity_cluster_count.items() if count >= 2]

    for entity_id in high_risk_entities:
        info = entity_info.get(entity_id, {})
        investigation_candidates.append({
            'entity_id': entity_id,
            'filing_number': info.get('filing_number'),
            'name': info.get('name'),
            'cluster_count': entity_cluster_count[entity_id],
            'violations': {
                'has_tax_forfeiture': info.get('has_tax_forfeiture', False),
                'has_forfeited_status': info.get('has_forfeited_status', False),
                'has_reinstatement': info.get('has_reinstatement', False)
            }
        })

    print(f"   Found {len(investigation_candidates)} high-risk entities")

    # Save results
    output_file = DATA_PROCESSED_DIR / "embedding_similarity_analysis.json"
    results = {
        'similarity_analysis': {
            'similarity_pairs': similarity_pairs[:50],  # Top 50 pairs
            'total_pairs': len(similarity_pairs),
            'threshold': similarity_results.get('threshold', 0.7)
        },
        'violation_clusters': clusters,
        'investigation_candidates': investigation_candidates,
        'summary': {
            'total_entities': len(entity_info),
            'similarity_pairs': len(similarity_pairs),
            'address_clusters': len(address_clusters),
            'agent_clusters': len(agent_clusters),
            'pattern_clusters': len(pattern_clusters),
            'high_risk_entities': len(investigation_candidates)
        },
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source': 'embedding_violation_analysis.py',
            'embedding_model': embeddings_data.get('metadata', {}).get('model', 'unknown')
        }
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Embedding analysis complete!")
    print(f"  Results saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  - Total entities analyzed: {len(entity_info)}")
    print(f"  - Similarity pairs found: {len(similarity_pairs)}")
    print(f"  - Address clusters: {len(address_clusters)}")
    print(f"  - Agent clusters: {len(agent_clusters)}")
    print(f"  - Violation pattern clusters: {len(pattern_clusters)}")
    print(f"  - High-risk entities: {len(investigation_candidates)}")


if __name__ == '__main__':
    main()
