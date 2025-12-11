#!/usr/bin/env python3
"""
Advanced Evidence-to-Law Matching with Multiple AI/ML Techniques
Uses ensemble methods, multiple similarity metrics, and form-based weighting
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR

# Optimize for ARM M4 MAX
MAX_WORKERS = os.cpu_count() or 16
BATCH_SIZE = 256  # Larger batches for better efficiency
print(f"🚀 Advanced Evidence-Law Matching - ARM M4 MAX Optimized ({MAX_WORKERS} workers)")

# Try to use faster libraries first, fallback to standard
try:
    import faiss  # Facebook AI Similarity Search - much faster for vector operations
    FAISS_AVAILABLE = True
    print("✅ FAISS available for fast vector similarity")
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available, using NumPy (install with: pip install faiss-cpu)")

try:
    from numba import jit, prange  # JIT compilation for speed
    NUMBA_AVAILABLE = True
    print("✅ Numba available for JIT acceleration")
except ImportError:
    NUMBA_AVAILABLE = False
    print("⚠️  Numba not available (install with: pip install numba)")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import scipy.spatial.distance as distance
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# Install missing libraries
if not SENTENCE_TRANSFORMERS_AVAILABLE or not SKLEARN_AVAILABLE or not SCIPY_AVAILABLE:
    print("Installing required ML libraries...")
    import subprocess
    packages = ["sentence-transformers", "scikit-learn", "numpy", "scipy"]
    if not FAISS_AVAILABLE:
        packages.append("faiss-cpu")
    if not NUMBA_AVAILABLE:
        packages.append("numba")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user"] + packages,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Re-import after installation
    try:
        import faiss
        FAISS_AVAILABLE = True
    except:
        FAISS_AVAILABLE = False

    try:
        from numba import jit, prange
        NUMBA_AVAILABLE = True
    except:
        NUMBA_AVAILABLE = False

    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import scipy.spatial.distance as distance
    print("✅ ML libraries installed")


class AdvancedEvidenceLawMatcher:
    """Advanced ML system for matching evidence to ground truth laws with form-based weighting"""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))

    def load_data(self):
        """Load violations, laws, and forms"""
        print("\n📂 Loading data...")

        # Load violations
        violations_file = DATA_PROCESSED_DIR / "integrated_violations.json"
        if violations_file.exists():
            with open(violations_file, 'r', encoding='utf-8') as f:
                self.violations = json.load(f)

        # Load laws
        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        if law_file.exists():
            with open(law_file, 'r', encoding='utf-8') as f:
                self.laws = json.load(f)

        # Extract forms from laws
        self._extract_forms()

        violations_count = sum(len(v) for v in self.violations.get('violations', {}).values())
        print(f"   Loaded violations: {violations_count}")
        print(f"   Loaded laws")
        print(f"   Loaded forms: {len(self.forms)}")

    def _extract_forms(self):
        """Extract all reporting forms from laws"""
        def extract_forms_recursive(data, path=""):
            if isinstance(data, dict):
                if "reporting_forms" in data:
                    for form in data["reporting_forms"]:
                        form_id = form.get("form_number") or form.get("form_name", "unknown")
                        self.forms[form_id] = {
                            **form,
                            "law": data.get("name", ""),
                            "path": path
                        }
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        extract_forms_recursive(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_forms_recursive(item, f"{path}[{i}]")

        extract_forms_recursive(self.laws)

    def create_evidence_text(self, violation: Dict[str, Any]) -> str:
        """Create comprehensive evidence text for matching"""
        parts = []
        parts.append(f"VIOLATION_TYPE: {violation.get('violation_type', '')}")
        parts.append(f"ENTITY: {violation.get('entity_name', '')}")
        parts.append(f"DESCRIPTION: {violation.get('description', '')}")
        parts.append(f"SEVERITY: {violation.get('severity', '')}")
        if violation.get('jurisdiction'):
            parts.append(f"JURISDICTION: {violation['jurisdiction']}")
        if violation.get('state'):
            parts.append(f"STATE: {violation['state']}")
        if violation.get('source'):
            parts.append(f"SOURCE: {violation['source']}")
        return " | ".join(parts)

    def extract_law_embeddings(self) -> Dict[str, Dict]:
        """Extract all law embeddings (prioritize ground truth)"""
        print("\n🔍 Extracting law embeddings...")

        law_embeddings = {}

        def extract_laws_recursive(data, path=""):
            if isinstance(data, dict):
                # Prioritize ground truth embeddings
                if "ground_truth_embedding" in data and "ground_truth_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["ground_truth_embedding"]),
                        "text": data["ground_truth_text"],
                        "law_data": data,
                        "is_ground_truth": True
                    }
                elif "embedding" in data and "embedding_text" in data:
                    law_id = f"law_{path}"
                    law_embeddings[law_id] = {
                        "embedding": np.array(data["embedding"]),
                        "text": data["embedding_text"],
                        "law_data": data,
                        "is_ground_truth": False
                    }

                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        extract_laws_recursive(value, f"{path}.{key}" if path else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_laws_recursive(item, f"{path}[{i}]")

        extract_laws_recursive(self.laws)

        print(f"   Extracted {len(law_embeddings)} law embeddings")
        return law_embeddings

    def compute_multiple_similarities(self, evidence_embedding: np.ndarray,
                                     law_embedding: np.ndarray) -> Dict[str, float]:
        """Compute multiple similarity metrics using optimized implementations"""
        similarities = {}

        # Use optimized NumPy operations
        evidence_norm = np.linalg.norm(evidence_embedding)
        law_norm = np.linalg.norm(law_embedding)
        dot_product = np.dot(evidence_embedding, law_embedding)

        # 1. Cosine Similarity (optimized)
        if evidence_norm > 0 and law_norm > 0:
            similarities["cosine"] = float(dot_product / (evidence_norm * law_norm))
        else:
            similarities["cosine"] = 0.0

        # 2. Euclidean Distance (vectorized, inverted)
        diff = evidence_embedding - law_embedding
        euclidean_dist = np.sqrt(np.dot(diff, diff))  # Faster than np.linalg.norm
        similarities["euclidean"] = float(1 / (1 + euclidean_dist))

        # 3. Manhattan Distance (vectorized)
        manhattan_dist = np.sum(np.abs(diff))
        similarities["manhattan"] = float(1 / (1 + manhattan_dist))

        # 4. Dot Product (already computed)
        similarities["dot_product"] = float(dot_product)

        # 5. Jaccard Similarity (optimized with vectorized operations)
        evidence_binary = (evidence_embedding > 0)
        law_binary = (law_embedding > 0)
        intersection = np.sum(evidence_binary & law_binary)
        union = np.sum(evidence_binary | law_binary)
        similarities["jaccard"] = float(intersection / union) if union > 0 else 0.0

        # 6. Pearson Correlation (vectorized)
        if len(evidence_embedding) > 1:
            try:
                # Use optimized correlation computation
                evidence_mean = np.mean(evidence_embedding)
                law_mean = np.mean(law_embedding)
                evidence_centered = evidence_embedding - evidence_mean
                law_centered = law_embedding - law_mean
                numerator = np.dot(evidence_centered, law_centered)
                denominator = np.sqrt(np.dot(evidence_centered, evidence_centered) *
                                    np.dot(law_centered, law_centered))
                correlation = numerator / denominator if denominator > 0 else 0.0
                similarities["pearson"] = float(correlation) if not np.isnan(correlation) else 0.0
            except:
                similarities["pearson"] = 0.0
        else:
            similarities["pearson"] = 0.0

        return similarities

    def compute_tfidf_similarity(self, evidence_text: str, law_text: str) -> float:
        """Compute TF-IDF similarity"""
        try:
            texts = [evidence_text, law_text]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0

    def compute_form_weight(self, violation: Dict[str, Any], law_data: Dict[str, Any]) -> float:
        """Compute weight based on available reporting forms"""
        forms = law_data.get("reporting_forms", [])
        if not forms:
            return 0.5  # Default weight if no forms

        violation_type = violation.get("violation_type", "").lower()
        jurisdiction = violation.get("jurisdiction", "").lower()
        severity = violation.get("severity", "").upper()

        weight = 0.5  # Base weight

        # More forms = higher weight
        weight += min(0.2, len(forms) * 0.05)

        # Check form relevance to violation
        for form in forms:
            form_desc = form.get("description", "").lower()
            form_name = form.get("form_name", "").lower()

            if any(term in form_desc or term in form_name for term in violation_type.split()):
                weight += 0.1

            form_agency = form.get("agency", "").lower()
            if jurisdiction in form_agency or form_agency in jurisdiction:
                weight += 0.1

        # Higher severity = higher weight
        if severity == "HIGH":
            weight += 0.1
        elif severity == "MEDIUM":
            weight += 0.05

        return min(1.0, weight)

    def ensemble_match(self, evidence_text: str, evidence_embedding: np.ndarray,
                      law_embeddings: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Use ensemble of ML techniques to match evidence to laws"""
        matches = []

        for law_id, law_info in law_embeddings.items():
            law_embedding = law_info["embedding"]
            law_text = law_info["text"]
            law_data = law_info["law_data"]

            # Compute multiple similarity metrics
            similarities = self.compute_multiple_similarities(evidence_embedding, law_embedding)

            # TF-IDF similarity
            tfidf_sim = self.compute_tfidf_similarity(evidence_text, law_text)
            similarities["tfidf"] = tfidf_sim

            # Form-based weight
            violation_dict = {
                "violation_type": evidence_text.split("VIOLATION_TYPE:")[1].split("|")[0].strip() if "VIOLATION_TYPE:" in evidence_text else "",
                "jurisdiction": evidence_text.split("JURISDICTION:")[1].split("|")[0].strip() if "JURISDICTION:" in evidence_text else "",
                "severity": evidence_text.split("SEVERITY:")[1].split("|")[0].strip() if "SEVERITY:" in evidence_text else "MEDIUM"
            }
            form_weight = self.compute_form_weight(violation_dict, law_data)

            # Ensemble score (weighted combination)
            ensemble_score = (
                0.30 * similarities["cosine"] +
                0.15 * similarities["euclidean"] +
                0.10 * similarities["manhattan"] +
                0.10 * similarities["dot_product"] +
                0.10 * similarities["jaccard"] +
                0.10 * similarities["pearson"] +
                0.10 * similarities["tfidf"] +
                0.05 * form_weight
            )

            # Ground truth bonus
            if law_info.get("is_ground_truth"):
                ensemble_score *= 1.1

            matches.append({
                "law_id": law_id,
                "law_name": law_data.get("name", ""),
                "ensemble_score": ensemble_score,
                "similarities": similarities,
                "form_weight": form_weight,
                "is_ground_truth": law_info.get("is_ground_truth", False),
                "law_data": law_data
            })

        matches.sort(key=lambda x: x["ensemble_score"], reverse=True)
        return matches

    def match_all_evidence_fast(self, top_k: int = 5) -> Dict[str, Any]:
        """Fast matching using FAISS for vector similarity search"""
        print("\n🔗 Fast matching using FAISS vector similarity search...")

        law_embeddings = self.extract_law_embeddings()

        if FAISS_AVAILABLE and len(law_embeddings) > 0:
            # Build FAISS index for fast similarity search
            dimension = len(list(law_embeddings.values())[0]["embedding"])
            index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity for normalized vectors)

            # Add law embeddings to index
            law_ids = []
            law_vectors = []
            for law_id, law_info in law_embeddings.items():
                law_vectors.append(law_info["embedding"].astype('float32'))
                law_ids.append(law_id)

            law_matrix = np.vstack(law_vectors)
            index.add(law_matrix)

            print(f"   Built FAISS index with {index.ntotal} vectors")

        violations_data = self.violations.get("violations", {})
        all_matches = []

        # Batch encode all evidence at once (much faster)
        print("   Encoding all evidence in batch...")
        evidence_texts = []
        evidence_metadata = []
        for category, items in violations_data.items():
            for item in items:
                evidence_text = self.create_evidence_text(item)
                evidence_texts.append(evidence_text)
                evidence_metadata.append({
                    "violation": item,
                    "category": category,
                    "text": evidence_text
                })

        # Batch encode (leverage 128GB RAM)
        evidence_embeddings = self.model.encode(evidence_texts, normalize_embeddings=True,
                                                batch_size=BATCH_SIZE, show_progress_bar=False,
                                                convert_to_numpy=True)

        print(f"   Processing {len(evidence_texts)} evidence items...")

        def process_evidence_fast_batch(batch_indices, evidence_embeddings_array, law_embeddings_dict, law_ids_list):
            """Process batch using FAISS for fast similarity search"""
            batch_matches = []

            for idx in batch_indices:
                evidence_embedding = evidence_embeddings_array[idx]
                evidence_meta = evidence_metadata[idx]

                if FAISS_AVAILABLE:
                    # Use FAISS for fast similarity search
                    evidence_vector = evidence_embedding.astype('float32').reshape(1, -1)
                    similarities, indices = index.search(evidence_vector, min(top_k * 2, len(law_ids)))  # Get more for filtering

                    matches = []
                    for sim_score, law_idx in zip(similarities[0], indices[0]):
                        if law_idx < len(law_ids):
                            law_id = law_ids_list[law_idx]
                            law_info = law_embeddings_dict[law_id]

                            # Compute additional metrics for top matches
                            law_embedding = law_info["embedding"]
                            additional_sims = self.compute_multiple_similarities(evidence_embedding, law_embedding)

                            # Form weight
                            violation_dict = {
                                "violation_type": evidence_meta["text"].split("VIOLATION_TYPE:")[1].split("|")[0].strip() if "VIOLATION_TYPE:" in evidence_meta["text"] else "",
                                "jurisdiction": evidence_meta["text"].split("JURISDICTION:")[1].split("|")[0].strip() if "JURISDICTION:" in evidence_meta["text"] else "",
                                "severity": evidence_meta["text"].split("SEVERITY:")[1].split("|")[0].strip() if "SEVERITY:" in evidence_meta["text"] else "MEDIUM"
                            }
                            form_weight = self.compute_form_weight(violation_dict, law_info["law_data"])

                            # Ensemble score
                            ensemble_score = (
                                0.30 * additional_sims["cosine"] +
                                0.15 * additional_sims["euclidean"] +
                                0.10 * additional_sims["manhattan"] +
                                0.10 * additional_sims["dot_product"] +
                                0.10 * additional_sims["jaccard"] +
                                0.10 * additional_sims["pearson"] +
                                0.10 * self.compute_tfidf_similarity(evidence_meta["text"], law_info["text"]) +
                                0.05 * form_weight
                            )

                            if law_info.get("is_ground_truth"):
                                ensemble_score *= 1.1

                            matches.append({
                                "law_id": law_id,
                                "law_name": law_info["law_data"].get("name", ""),
                                "ensemble_score": ensemble_score,
                                "similarities": additional_sims,
                                "form_weight": form_weight,
                                "is_ground_truth": law_info.get("is_ground_truth", False),
                                "law_data": law_info["law_data"]
                            })

                    matches.sort(key=lambda x: x["ensemble_score"], reverse=True)
                    batch_matches.append({
                        "violation": evidence_meta["violation"],
                        "category": evidence_meta["category"],
                        "matches": matches[:top_k]
                    })
                else:
                    # Fallback to original method
                    matches = self.ensemble_match(
                        evidence_meta["text"],
                        evidence_embedding,
                        law_embeddings_dict
                    )
                    batch_matches.append({
                        "violation": evidence_meta["violation"],
                        "category": evidence_meta["category"],
                        "matches": matches[:top_k]
                    })

            return batch_matches

        # Process in parallel batches
        batch_size = max(1, len(evidence_texts) // MAX_WORKERS)
        batch_indices = [list(range(i, min(i+batch_size, len(evidence_texts))))
                        for i in range(0, len(evidence_texts), batch_size)]

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            if FAISS_AVAILABLE:
                futures = [executor.submit(process_evidence_fast_batch, batch_idx,
                                          evidence_embeddings, law_embeddings, law_ids)
                          for batch_idx in batch_indices]
            else:
                # Fallback: create embeddings dict for each evidence
                evidence_embeddings_dict = {i: emb for i, emb in enumerate(evidence_embeddings)}
                futures = [executor.submit(process_evidence_fast_batch, batch_idx,
                                          evidence_embeddings, law_embeddings, law_ids)
                          for batch_idx in batch_indices]

            completed = 0
            for future in as_completed(futures):
                try:
                    batch_matches = future.result()
                    all_matches.extend(batch_matches)
                    completed += len(batch_matches)
                    if completed % 20 == 0:
                        print(f"   Progress: {completed}/{len(evidence_texts)} evidence items processed")
                except Exception as e:
                    print(f"   ⚠️  Error in batch: {e}")

        print(f"✅ Matched {len(all_matches)} evidence items to laws")

        return {
            "matched_evidence": all_matches,
            "total_evidence": len(evidence_texts),
            "total_laws": len(law_embeddings),
            "techniques_used": [
                "cosine_similarity",
                "euclidean_distance",
                "manhattan_distance",
                "dot_product",
                "jaccard_similarity",
                "pearson_correlation",
                "tfidf_similarity",
                "form_based_weighting",
                "ground_truth_bonus",
                "ensemble_scoring",
                "faiss_vector_search" if FAISS_AVAILABLE else "numpy_vector_search",
                "batch_encoding" if BATCH_SIZE > 1 else "sequential_encoding"
            ]
        }

    def match_all_evidence(self, top_k: int = 5) -> Dict[str, Any]:
        """Match all evidence to laws - uses fast method if available"""
        return self.match_all_evidence_fast(top_k)

    def generate_ml_analysis_report(self, matches: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive ML analysis report"""
        print("\n📊 Generating ML analysis report...")

        all_scores = [
            m["ensemble_score"]
            for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
        ]

        avg_score = np.mean(all_scores) if all_scores else 0.0

        form_weighted_matches = [
            m for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
            if m["form_weight"] > 0.6
        ]

        ground_truth_matches = [
            m for evidence in matches["matched_evidence"]
            for m in evidence["matches"]
            if m["is_ground_truth"]
        ]

        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "model": "all-MiniLM-L6-v2",
                "techniques": matches["techniques_used"],
                "parallel_workers": MAX_WORKERS,
                "batch_size": BATCH_SIZE
            },
            "statistics": {
                "total_evidence": matches["total_evidence"],
                "total_laws": matches["total_laws"],
                "total_matches": sum(len(m["matches"]) for m in matches["matched_evidence"]),
                "average_ensemble_score": float(avg_score),
                "form_weighted_matches": len(form_weighted_matches),
                "ground_truth_matches": len(ground_truth_matches)
            },
            "matches": matches["matched_evidence"]
        }

        return report


def main():
    """Main function"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("🤖 Advanced Evidence-Law Matching with Multiple AI/ML Techniques")
    print("=" * 80)
    print(f"Architecture: ARM M4 MAX")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Batch Size: {BATCH_SIZE}")
    print("=" * 80)
    print()

    matcher = AdvancedEvidenceLawMatcher()
    matcher.load_data()

    matches = matcher.match_all_evidence(top_k=5)

    report = matcher.generate_ml_analysis_report(matches)

    output_file = DATA_PROCESSED_DIR / "advanced_evidence_law_matching.json"
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("✅ Advanced Evidence-Law Matching Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Evidence items: {report['statistics']['total_evidence']}")
    print(f"Laws matched: {report['statistics']['total_laws']}")
    print(f"Total matches: {report['statistics']['total_matches']}")
    print(f"Average ensemble score: {report['statistics']['average_ensemble_score']:.4f}")
    print(f"Form-weighted matches: {report['statistics']['form_weighted_matches']}")
    print(f"Ground truth matches: {report['statistics']['ground_truth_matches']}")
    print(f"Techniques used: {len(report['metadata']['techniques'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()
