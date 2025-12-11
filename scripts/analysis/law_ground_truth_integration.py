#!/usr/bin/env python3
"""
Law Ground Truth Integration System
Integrates law references (federal, state, local) with violations data
Uses laws as ground truth for violation analysis
Includes ML pipeline for violation-law matching
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

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR, RESEARCH_DIR, DATA_RAW_DIR

try:
    from sentence_transformers import SentenceTransformer
    import sklearn
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "sentence-transformers", "scikit-learn", "numpy"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer
    import sklearn
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import DBSCAN
    from sklearn.decomposition import PCA


class LawGroundTruthSystem:
    """System for integrating law references as ground truth with violations"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.law_references = {}
        self.violations = {}
        self.lariat_embeddings = {}
        self.research_intersections = {}
        self.matched_violations = []

    def load_law_references(self, law_file: Path) -> Dict[str, Any]:
        """Load law references from JSON file"""
        print(f"Loading law references from {law_file}...")
        try:
            with open(law_file, 'r', encoding='utf-8') as f:
                self.law_references = json.load(f)
            print(f"✅ Loaded law references")
            return self.law_references
        except FileNotFoundError:
            print(f"⚠️  Law references file not found. Creating new one...")
            return self._create_law_references()
        except Exception as e:
            print(f"❌ Error loading law references: {e}")
            return {}

    def _create_law_references(self) -> Dict[str, Any]:
        """Create law references if they don't exist"""
        # Import and run the create_law_references script
        from scripts.utils.create_law_references import create_jurisdiction_references, add_embeddings_recursive

        print("Creating new law references...")
        references = create_jurisdiction_references()
        add_embeddings_recursive(references, self.model)

        # Save to file
        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        law_file.parent.mkdir(parents=True, exist_ok=True)
        with open(law_file, 'w', encoding='utf-8') as f:
            json.dump(references, f, indent=2, ensure_ascii=False)

        self.law_references = references
        return references

    def load_violations(self, violations_file: Path) -> Dict[str, Any]:
        """Load violations data"""
        print(f"Loading violations from {violations_file}...")
        try:
            with open(violations_file, 'r', encoding='utf-8') as f:
                self.violations = json.load(f)
            print(f"✅ Loaded {len(self.violations.get('violations', {}))} violation categories")
            return self.violations
        except Exception as e:
            print(f"❌ Error loading violations: {e}")
            return {}

    def load_lariat_embeddings(self, embeddings_file: Path) -> Dict[str, Any]:
        """Load Lariat TX embeddings"""
        print(f"Loading Lariat embeddings from {embeddings_file}...")
        try:
            with open(embeddings_file, 'r', encoding='utf-8') as f:
                self.lariat_embeddings = json.load(f)
            print(f"✅ Loaded {len(self.lariat_embeddings.get('vectors', []))} Lariat embeddings")
            return self.lariat_embeddings
        except Exception as e:
            print(f"❌ Error loading Lariat embeddings: {e}")
            return {}

    def load_lariat_txt(self, txt_file: Path) -> str:
        """Load raw Lariat text data"""
        print(f"Loading Lariat text from {txt_file}...")
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Loaded {len(content)} characters from Lariat text")
            return content
        except Exception as e:
            print(f"❌ Error loading Lariat text: {e}")
            return ""

    def extract_law_embeddings(self) -> List[Dict[str, Any]]:
        """Extract all law embeddings from references (ground truth citations)"""
        law_vectors = []

        def extract_recursive(data: Any, path: str = ""):
            if isinstance(data, dict):
                if "embedding" in data and "embedding_text" in data:
                    # This is a ground truth law reference
                    law_vectors.append({
                        "path": path,
                        "text": data.get("embedding_text", ""),
                        "embedding": data.get("embedding", []),
                        "name": data.get("name", ""),
                        "description": data.get("description", ""),
                        "url": data.get("url", ""),
                        "relevance": data.get("relevance", ""),
                        "key_sections": data.get("key_sections", []),
                        "reporting_forms": data.get("reporting_forms", []),
                        "is_ground_truth": True,  # Mark as ground truth
                        "authoritative": True,
                        "full_citations": data.get("key_sections", [])  # Full law citations
                    })
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text"]:
                        new_path = f"{path}.{key}" if path else key
                        extract_recursive(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_path = f"{path}[{i}]"
                    extract_recursive(item, new_path)

        extract_recursive(self.law_references)
        print(f"✅ Extracted {len(law_vectors)} ground truth law embeddings")
        return law_vectors

    def process_research_intersections(self, max_files: int = 100) -> Dict[str, Any]:
        """Process recursive intersections from research directory (optimized with limits)"""
        print("Processing research intersections...")
        intersections = {
            "entities": [],
            "violations": [],
            "licenses": [],
            "connections": []
        }

        # Process license searches (limit to avoid processing too many files)
        license_dir = RESEARCH_DIR / "license_searches" / "data"
        file_count = 0
        if license_dir.exists():
            for state_dir in license_dir.iterdir():
                if state_dir.is_dir() and file_count < max_files:
                    state_name = state_dir.name
                    for json_file in list(state_dir.glob("*.json"))[:20]:  # Limit per state
                        if file_count >= max_files:
                            break
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                intersections["licenses"].append({
                                    "state": state_name,
                                    "file": str(json_file.relative_to(RESEARCH_DIR)),
                                    "data": data
                                })
                                file_count += 1
                        except Exception as e:
                            print(f"⚠️  Error reading {json_file}: {e}")

        # Process violations from research
        violations_dir = RESEARCH_DIR / "reports"
        if violations_dir.exists():
            for md_file in violations_dir.glob("*VIOLATION*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        intersections["violations"].append({
                            "file": str(md_file.relative_to(RESEARCH_DIR)),
                            "content": content[:1000]  # First 1000 chars
                        })
                except Exception as e:
                    print(f"⚠️  Error reading {md_file}: {e}")

        # Process connections
        connections_file = RESEARCH_DIR / "connections" / "caitlin_skidmore_connections.json"
        if connections_file.exists():
            try:
                with open(connections_file, 'r', encoding='utf-8') as f:
                    intersections["connections"] = json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading connections: {e}")

        self.research_intersections = intersections
        print(f"✅ Processed research intersections:")
        print(f"   - Licenses: {len(intersections['licenses'])}")
        print(f"   - Violations: {len(intersections['violations'])}")
        print(f"   - Connections: {len(intersections.get('connections', []))}")
        return intersections

    def match_violations_to_laws(self, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Match violations to relevant laws using cosine similarity
        Laws serve as ground truth - violations are matched against authoritative law citations"""
        print(f"Matching violations to ground truth laws (threshold: {threshold})...")
        print(f"   Using full law citations as authoritative reference...")

        law_vectors = self.extract_law_embeddings()
        if not law_vectors:
            print("⚠️  No law vectors found")
            return []

        # Extract violation embeddings
        violation_vectors = []
        if "vectors" in self.lariat_embeddings:
            for vec in self.lariat_embeddings["vectors"]:
                violation_vectors.append({
                    "id": vec.get("id", ""),
                    "text": vec.get("text", ""),
                    "embedding": vec.get("embedding", []),
                    "source": "lariat_embeddings"
                })

        # Also create embeddings for violations from extracted_violations.json
        violations_data = self.violations.get("violations", {})
        for category, items in violations_data.items():
            for item in items:
                violation_text = self._create_violation_text(item)
                embedding = self.model.encode(violation_text, normalize_embeddings=True)
                violation_vectors.append({
                    "id": f"violation_{category}_{item.get('entity_name', 'unknown')}",
                    "text": violation_text,
                    "embedding": embedding.tolist(),
                    "violation_data": item,
                    "source": "extracted_violations"
                })

        # Match violations to laws - find top 3 matches per violation
        matches = []
        for violation in violation_vectors:
            if not violation.get("embedding"):
                continue

            violation_emb = np.array(violation["embedding"]).reshape(1, -1)
            law_scores = []

            for law in law_vectors:
                if not law.get("embedding"):
                    continue

                law_emb = np.array(law["embedding"]).reshape(1, -1)
                similarity = cosine_similarity(violation_emb, law_emb)[0][0]

                law_scores.append({
                    "law": law,
                    "similarity": float(similarity)
                })

            # Sort by similarity and take top matches above threshold
            law_scores.sort(key=lambda x: x["similarity"], reverse=True)
            for score_data in law_scores[:3]:  # Top 3 matches
                if score_data["similarity"] >= threshold:
                    matches.append({
                        "violation": violation,
                        "law": score_data["law"],
                        "similarity": score_data["similarity"],
                        "matched_at": datetime.now().isoformat()
                    })

        self.matched_violations = matches
        print(f"✅ Matched {len(matches)} violations to laws")
        return matches

    def _create_violation_text(self, violation: Dict[str, Any]) -> str:
        """Create text representation of violation for embedding"""
        parts = []

        # Include violation type with context
        violation_type = violation.get("violation_type", "")
        if violation_type:
            parts.append(f"Violation: {violation_type}")
            # Add context based on violation type
            if "tax" in violation_type.lower() or "forfeiture" in violation_type.lower():
                parts.append("Tax violation, tax forfeiture, failure to pay taxes, tax fraud")
            if "filing" in violation_type.lower() or "late" in violation_type.lower():
                parts.append("Late filing, failure to file, regulatory compliance")
            if "forfeited" in violation_type.lower():
                parts.append("Entity forfeiture, business entity violation, corporate compliance")

        if violation.get("entity_name"):
            parts.append(f"Entity: {violation['entity_name']}")
        if violation.get("description"):
            parts.append(f"Description: {violation['description']}")
        if violation.get("severity"):
            parts.append(f"Severity: {violation['severity']}")
        if violation.get("filing_date"):
            parts.append(f"Filing Date: {violation['filing_date']}")
        if violation.get("filing_type"):
            parts.append(f"Filing Type: {violation['filing_type']}")

        return " | ".join(parts)

    def cluster_violations(self, eps: float = 0.5, min_samples: int = 2) -> Dict[str, Any]:
        """Cluster violations using DBSCAN"""
        print(f"Clustering violations (eps={eps}, min_samples={min_samples})...")

        if not self.matched_violations:
            print("⚠️  No matched violations to cluster")
            return {}

        # Extract embeddings
        embeddings = []
        violation_ids = []
        for match in self.matched_violations:
            violation = match["violation"]
            if violation.get("embedding"):
                embeddings.append(violation["embedding"])
                violation_ids.append(violation.get("id", ""))

        if len(embeddings) < 2:
            print("⚠️  Not enough violations to cluster")
            return {}

        embeddings_array = np.array(embeddings)

        # Apply DBSCAN
        clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        cluster_labels = clustering.fit_predict(embeddings_array)

        # Organize results
        clusters = defaultdict(list)
        for i, label in enumerate(cluster_labels):
            if label != -1:  # -1 is noise in DBSCAN
                clusters[f"cluster_{label}"].append({
                    "violation_id": violation_ids[i],
                    "match": self.matched_violations[i]
                })

        print(f"✅ Found {len(clusters)} clusters ({sum(1 for l in cluster_labels if l == -1)} noise points)")
        return {
            "clusters": dict(clusters),
            "n_clusters": len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
            "n_noise": sum(1 for l in cluster_labels if l == -1)
        }

    def generate_ml_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive ML analysis"""
        print("Generating ML analysis...")

        analysis = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "model": "all-MiniLM-L6-v2",
                "dimension": 384
            },
            "summary": {
                "total_laws": len(self.extract_law_embeddings()),
                "total_violations": len(self.matched_violations),
                "matched_violations": len(self.matched_violations),
                "research_intersections": {
                    "licenses": len(self.research_intersections.get("licenses", [])),
                    "violations": len(self.research_intersections.get("violations", [])),
                    "connections": len(self.research_intersections.get("connections", []))
                }
            },
            "violation_law_matches": self.matched_violations,
            "research_intersections": self.research_intersections,
            "clusters": self.cluster_violations()
        }

        return analysis

    def save_results(self, output_file: Path):
        """Save all results to JSON file"""
        print(f"Saving results to {output_file}...")

        results = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "system": "Law Ground Truth Integration",
                "version": "1.0.0"
            },
            "law_references_summary": {
                "federal_criminal": len(self.law_references.get("federal", {}).get("criminal", {})),
                "federal_civil": len(self.law_references.get("federal", {}).get("civil", {})),
                "states": len(self.law_references.get("states", {})),
                "localities": len(self.law_references.get("localities", {}))
            },
            "violations_summary": {
                "categories": list(self.violations.get("violations", {}).keys()),
                "total_violations": sum(len(v) for v in self.violations.get("violations", {}).values())
            },
            "matched_violations": self.matched_violations,
            "research_intersections": self.research_intersections,
            "ml_analysis": self.generate_ml_analysis()
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved results to {output_file}")


def main():
    """Main execution function"""
    print("=" * 80)
    print("Law Ground Truth Integration System")
    print("=" * 80)

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

    # Process research intersections
    system.process_research_intersections()

    # Match violations to laws
    system.match_violations_to_laws(threshold=0.7)

    # Generate ML analysis
    ml_analysis = system.generate_ml_analysis()

    # Save results
    output_file = DATA_PROCESSED_DIR / "law_ground_truth_integration.json"
    system.save_results(output_file)

    print("\n" + "=" * 80)
    print("✅ Integration Complete!")
    print("=" * 80)
    print(f"Results saved to: {output_file}")
    print(f"Matched violations: {len(system.matched_violations)}")
    print(f"Law references: {len(system.extract_law_embeddings())}")


if __name__ == "__main__":
    main()
