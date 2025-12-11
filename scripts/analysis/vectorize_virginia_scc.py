#!/usr/bin/env python3
"""
Vectorize Virginia SCC filings and find abnormalities using semantic similarity
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import numpy as np
from typing import List, Dict, Any

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

def load_virginia_scc_data() -> Dict[str, Any]:
    """Load Virginia SCC raw data"""
    raw_file = PROJECT_ROOT / "data" / "raw" / "virginia_scc_kettler_filings.json"
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw data file not found: {raw_file}")

    with open(raw_file, 'r') as f:
        return json.load(f)

def create_text_representations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create text representations for embedding"""
    texts = []

    for entity in data.get("entities_found", []):
        # Create comprehensive text representation
        text_parts = [
            f"Entity ID: {entity.get('entity_id', 'N/A')}",
            f"Legal Name: {entity.get('legal_name', 'N/A')}",
            f"Fictitious Name: {entity.get('fictitious_name', 'N/A')}",
            f"Name Type: {entity.get('name_type', 'N/A')}",
            f"Entity Type: {entity.get('entity_type', 'N/A')}",
            f"Status: {entity.get('status', 'N/A')}",
            f"Business Address: {entity.get('business_address', 'N/A')}",
            f"Registered Agent: {entity.get('registered_agent', 'N/A')}",
            f"Formation Date: {entity.get('formation_date', 'N/A')}",
            f"Last Annual Report: {entity.get('last_annual_report', 'N/A')}",
            f"Notes: {entity.get('notes', 'N/A')}"
        ]

        full_text = " | ".join(text_parts)

        texts.append({
            "entity_id": entity.get("entity_id"),
            "text": full_text,
            "metadata": entity
        })

    return texts

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """Generate embeddings for texts"""
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print(f"Generating embeddings for {len(texts)} texts...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    return embeddings

def find_similar_entities(embeddings: np.ndarray, threshold: float = 0.85) -> List[Dict[str, Any]]:
    """Find similar entities using cosine similarity"""
    similarities = []

    # Calculate cosine similarity matrix
    similarity_matrix = np.dot(embeddings, embeddings.T)

    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            similarity = float(similarity_matrix[i][j])
            if similarity >= threshold:
                similarities.append({
                    "entity_1_index": i,
                    "entity_2_index": j,
                    "similarity": similarity
                })

    return similarities

def analyze_abnormalities(data: Dict[str, Any], embeddings: np.ndarray, texts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze data for abnormalities using embeddings and semantic analysis"""
    abnormalities = []

    # 1. Check for name variations
    entity = data["entities_found"][0]
    legal_name = entity.get("legal_name", "").upper()
    fictitious_name = entity.get("fictitious_name", "").upper()

    if legal_name and fictitious_name:
        # Check if names are semantically similar but legally different
        name_embedding = generate_embeddings([legal_name, fictitious_name])
        name_similarity = float(np.dot(name_embedding[0], name_embedding[1]))

        if name_similarity > 0.9:
            abnormalities.append({
                "category": "Name Semantic Similarity",
                "severity": "Medium",
                "description": f"Legal name '{legal_name}' and fictitious name '{fictitious_name}' are semantically very similar (similarity: {name_similarity:.3f}) but use different corporate suffixes (INC vs CORP)",
                "similarity_score": name_similarity,
                "implication": "High semantic similarity suggests intentional name variation, potentially for regulatory or business purposes"
            })

    # 2. Check address patterns
    address = entity.get("business_address", "")
    if address:
        # Check for common address patterns that might indicate shell companies
        address_lower = address.lower()
        if "ste" in address_lower or "suite" in address_lower:
            abnormalities.append({
                "category": "Address Pattern",
                "severity": "Low",
                "description": "Business address uses suite/ste designation, which is common for office buildings",
                "address": address,
                "implication": "Standard practice, but verify if this is actual business location vs. mail forwarding"
            })

    # 3. Check registered agent pattern
    registered_agent = entity.get("registered_agent", "")
    if registered_agent:
        agent_lower = registered_agent.lower()
        if "registered agents" in agent_lower or "ra" in agent_lower:
            abnormalities.append({
                "category": "Registered Agent Pattern",
                "severity": "Low",
                "description": "Uses commercial registered agent service",
                "registered_agent": registered_agent,
                "implication": "Common practice for privacy/legal purposes, but may obscure actual business location"
            })

    # 4. Check for missing critical information
    missing_fields = []
    if not entity.get("formation_date"):
        missing_fields.append("formation_date")
    if not entity.get("last_annual_report"):
        missing_fields.append("last_annual_report")

    if missing_fields:
        abnormalities.append({
            "category": "Missing Critical Information",
            "severity": "Medium",
            "description": f"Missing fields: {', '.join(missing_fields)}",
            "missing_fields": missing_fields,
            "implication": "Cannot verify entity history, compliance, or timeline without this information"
        })

    # 5. Semantic analysis of entity description
    entity_text = texts[0]["text"] if texts else ""
    if entity_text:
        # Check for suspicious patterns in text
        suspicious_keywords = ["shell", "holding", "dormant", "inactive", "dissolved"]
        text_lower = entity_text.lower()

        found_keywords = [kw for kw in suspicious_keywords if kw in text_lower]
        if found_keywords:
            abnormalities.append({
                "category": "Suspicious Keywords",
                "severity": "High",
                "description": f"Found suspicious keywords: {', '.join(found_keywords)}",
                "keywords": found_keywords,
                "implication": "May indicate shell company or inactive entity"
            })

    # 6. Check entity type consistency
    entity_type = entity.get("entity_type", "")
    if entity_type == "Stock Corporation":
        # Stock corporations typically have shareholders - check if this is mentioned
        if "stock" not in entity_text.lower() and "shareholder" not in entity_text.lower():
            abnormalities.append({
                "category": "Entity Type Details",
                "severity": "Low",
                "description": "Stock Corporation entity type but no shareholder information available",
                "entity_type": entity_type,
                "implication": "May need to verify shareholder structure"
            })

    return {
        "abnormalities": abnormalities,
        "total_abnormalities": len(abnormalities),
        "high_severity": len([a for a in abnormalities if a.get("severity") == "High"]),
        "medium_severity": len([a for a in abnormalities if a.get("severity") == "Medium"]),
        "low_severity": len([a for a in abnormalities if a.get("severity") == "Low"])
    }

def main():
    """Main function"""
    print("=" * 70)
    print("Virginia SCC Filings - Vector Analysis for Abnormalities")
    print("=" * 70)

    # Load data
    print("\n1. Loading Virginia SCC data...")
    data = load_virginia_scc_data()
    print(f"   ✓ Loaded data for {len(data.get('entities_found', []))} entities")

    # Create text representations
    print("\n2. Creating text representations...")
    texts = create_text_representations(data)
    print(f"   ✓ Created {len(texts)} text representations")

    # Generate embeddings
    print("\n3. Generating embeddings...")
    text_strings = [t["text"] for t in texts]
    embeddings = generate_embeddings(text_strings)
    print(f"   ✓ Generated embeddings (shape: {embeddings.shape})")

    # Analyze abnormalities
    print("\n4. Analyzing for abnormalities...")
    analysis = analyze_abnormalities(data, embeddings, texts)
    print(f"   ✓ Found {analysis['total_abnormalities']} abnormalities")
    print(f"     - High severity: {analysis['high_severity']}")
    print(f"     - Medium severity: {analysis['medium_severity']}")
    print(f"     - Low severity: {analysis['low_severity']}")

    # Save results
    output_file = PROJECT_ROOT / "research" / "analysis" / "virginia_scc_vector_analysis.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "source": "Virginia SCC Vector Analysis",
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimension": embeddings.shape[1] if len(embeddings.shape) > 1 else len(embeddings)
        },
        "embeddings": {
            "count": len(embeddings),
            "dimension": embeddings.shape[1] if len(embeddings.shape) > 1 else len(embeddings),
            "sample": embeddings[0].tolist() if len(embeddings) > 0 else []
        },
        "text_representations": texts,
        "abnormalities_analysis": analysis,
        "raw_data": data
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n5. Saving results to {output_file}")
    print(f"   ✓ Results saved")

    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)
    for i, abnormality in enumerate(analysis["abnormalities"], 1):
        print(f"\n{i}. {abnormality['category']} ({abnormality['severity']} Severity)")
        print(f"   {abnormality['description']}")
        if 'implication' in abnormality:
            print(f"   Implication: {abnormality['implication']}")

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
